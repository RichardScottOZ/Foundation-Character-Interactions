"""
LLM-Based Character Analysis
Alternative approach to traditional NLP for extracting characters and relationships
from literary texts using Large Language Models.

This demonstrates how LLMs can replace or augment the traditional NLTK-based approach.
"""

import json
import logging
from typing import List, Dict, Optional, Tuple
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LLMCharacterAnalyzer:
    """
    Analyzes characters and relationships in literary texts using LLM APIs.
    
    Supports multiple LLM providers:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Local models via Ollama
    """
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4", api_key: Optional[str] = None, temperature: float = 0.3):
        """
        Initialize the LLM-based character analyzer.
        
        Args:
            provider: LLM provider ("openai", "anthropic", "ollama")
            model: Model name (e.g., "gpt-4", "claude-3-opus", "llama2")
            api_key: API key for the provider (not needed for ollama)
            temperature: Temperature for LLM responses (0.0-1.0). Lower values are more deterministic.
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.temperature = temperature
        
        # Initialize client based on provider
        self.client = self._init_client()
    
    def _init_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            try:
                from openai import OpenAI
                return OpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
                return None
        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                return Anthropic(api_key=self.api_key)
            except ImportError:
                logger.error("Anthropic package not installed. Install with: pip install anthropic")
                return None
        elif self.provider == "ollama":
            try:
                import ollama
                return ollama
            except ImportError:
                logger.error("Ollama package not installed. Install with: pip install ollama")
                return None
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def extract_characters(self, text: str, chunk_size: int = 4000) -> List[Dict]:
        """
        Extract character names from text using LLM.
        
        Args:
            text: The text to analyze
            chunk_size: Maximum characters per chunk (for long texts)
            
        Returns:
            List of character dictionaries with name, frequency, and context
        """
        prompt = """Analyze the following text and extract all character names.
        
Rules:
1. Only include actual characters (people/beings), not places, titles, or organizations
2. Merge aliases and variations of the same character (e.g., "Hari" and "Hari Seldon" -> "Hari Seldon")
3. Exclude generic titles unless they refer to a specific unnamed character (e.g., "Master" if it's a specific person)
4. Provide a confidence score (0-1) for each character

Return the results as a JSON array with this structure:
[
  {
    "name": "Character Name",
    "aliases": ["alias1", "alias2"],
    "confidence": 0.95,
    "role": "protagonist/antagonist/supporting",
    "first_mention": "context of first appearance"
  }
]

Text to analyze:
{text}

Return only the JSON array, no additional commentary."""
        
        # Chunk text if needed
        chunks = self._chunk_text(text, chunk_size)
        all_characters = []
        
        for chunk in chunks:
            response = self._call_llm(prompt.format(text=chunk))
            try:
                characters = json.loads(response)
                all_characters.extend(characters)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse LLM response as JSON: {response[:100]}")
        
        # Merge characters across chunks
        merged_characters = self._merge_characters(all_characters)
        return merged_characters
    
    def analyze_relationships(self, text: str, characters: List[str]) -> Dict:
        """
        Analyze relationships between characters using LLM.
        
        Args:
            text: The text to analyze
            characters: List of character names to focus on
            
        Returns:
            Dictionary with relationship information
        """
        character_list = ", ".join(characters)
        prompt = f"""Analyze the relationships between these characters in the text:
{character_list}

For each pair of characters that interact, provide:
1. Nature of relationship (allies, enemies, family, neutral, romantic, etc.)
2. Strength of relationship (1-10)
3. Key interactions or scenes
4. How relationship evolves

Return as JSON:
{{
  "relationships": [
    {{
      "character1": "Name1",
      "character2": "Name2",
      "type": "relationship type",
      "strength": 8,
      "description": "brief description",
      "key_scenes": ["scene1", "scene2"]
    }}
  ]
}}

Text to analyze:
{text}

Return only the JSON, no additional commentary."""
        
        response = self._call_llm(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Could not parse relationships JSON: {response[:100]}")
            return {"relationships": []}
    
    def extract_character_traits(self, text: str, character_name: str) -> Dict:
        """
        Extract detailed traits and information about a specific character.
        
        Args:
            text: The text to analyze
            character_name: Name of the character to analyze
            
        Returns:
            Dictionary with character information
        """
        prompt = f"""Analyze the character "{character_name}" in the following text.

Provide:
1. Physical description (if mentioned)
2. Personality traits
3. Motivations and goals
4. Key actions and decisions
5. Character arc/development
6. Relationships with other characters

Return as JSON:
{{
  "name": "{character_name}",
  "physical_description": "...",
  "personality": ["trait1", "trait2"],
  "motivations": ["goal1", "goal2"],
  "key_actions": ["action1", "action2"],
  "character_arc": "description of development",
  "relationships": {{"character": "relationship type"}}
}}

Text:
{text}

Return only the JSON, no additional commentary."""
        
        response = self._call_llm(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Could not parse character traits JSON: {response[:100]}")
            return {"name": character_name, "error": "Could not parse response"}
    
    def _call_llm(self, prompt: str) -> str:
        """Call the configured LLM with the given prompt."""
        if not self.client:
            return '{"error": "LLM client not initialized"}'
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a literary analysis expert specializing in character analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                )
                return response.content[0].text
            
            elif self.provider == "ollama":
                response = self.client.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a literary analysis expert."},
                        {"role": "user", "content": prompt}
                    ],
                )
                return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return '{"error": "LLM call failed"}'
    
    def _chunk_text(self, text: str, chunk_size: int) -> List[str]:
        """
        Split text into chunks for processing.
        Uses sentence-aware splitting to preserve context boundaries.
        """
        chunks = []
        sentences = text.split('. ')  # Simple sentence splitting
        
        current_chunk = ""
        for sentence in sentences:
            # Add sentence to current chunk if it fits
            if len(current_chunk) + len(sentence) + 2 <= chunk_size:
                current_chunk += sentence + ". "
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]  # Return full text if no splitting occurred
    
    def _merge_characters(self, characters: List[Dict]) -> List[Dict]:
        """Merge duplicate characters from multiple chunks."""
        # Simple name-based merging - could be improved with fuzzy matching
        merged = {}
        for char in characters:
            name = char.get("name", "")
            if name in merged:
                # Update with higher confidence if available
                if char.get("confidence", 0) > merged[name].get("confidence", 0):
                    merged[name] = char
            else:
                merged[name] = char
        
        return list(merged.values())


def compare_with_traditional(traditional_names: List[str], llm_names: List[str]) -> Dict:
    """
    Compare results from traditional NLP vs LLM approach.
    
    Args:
        traditional_names: Character names from NLTK-based extraction
        llm_names: Character names from LLM-based extraction
        
    Returns:
        Comparison statistics
    """
    traditional_set = set(traditional_names)
    llm_set = set(llm_names)
    
    return {
        "traditional_only": list(traditional_set - llm_set),
        "llm_only": list(llm_set - traditional_set),
        "common": list(traditional_set & llm_set),
        "traditional_count": len(traditional_set),
        "llm_count": len(llm_set),
        "overlap_percentage": len(traditional_set & llm_set) / len(traditional_set | llm_set) * 100
    }


# Example usage
if __name__ == "__main__":
    print("LLM Character Analyzer - Example Usage\n")
    print("=" * 60)
    
    # Example text (excerpt from a story)
    sample_text = """
    Hari Seldon stood before the Galactic Emperor, his weathered face betraying 
    no emotion. The Emperor, Cleon I, leaned forward on his throne, studying 
    the mathematician carefully.
    
    "So, Seldon," the Emperor began, "you claim to predict the future?"
    
    Gaal Dornick, Seldon's young protégé, watched nervously from the side of 
    the chamber. He had only recently arrived on Trantor, the capital world, 
    and the sight of the Emperor was overwhelming.
    
    "Not predict, Your Highness," Hari replied calmly. "Psychohistory calculates 
    probabilities. The Empire will fall, not today or tomorrow, but fall it will."
    
    The Grand Vizier gasped at such treasonous words, but the Emperor merely 
    smiled. "Interesting," Cleon said. "Tell me more about this... Foundation you 
    propose."
    """
    
    print("Sample text length:", len(sample_text), "characters\n")
    
    print("To use this analyzer, you would:")
    print("1. Install required package: pip install openai")
    print("2. Set your API key: export OPENAI_API_KEY='your-key-here'")
    print("3. Initialize the analyzer:")
    print("   analyzer = LLMCharacterAnalyzer(provider='openai', model='gpt-4')")
    print("4. Extract characters:")
    print("   characters = analyzer.extract_characters(sample_text)")
    print("\n")
    
    print("Expected output structure:")
    expected_output = [
        {
            "name": "Hari Seldon",
            "aliases": ["Seldon", "Hari"],
            "confidence": 0.98,
            "role": "protagonist",
            "first_mention": "stood before the Galactic Emperor"
        },
        {
            "name": "Cleon I",
            "aliases": ["Emperor", "Cleon", "Your Highness"],
            "confidence": 0.95,
            "role": "supporting",
            "first_mention": "The Emperor, Cleon I, leaned forward"
        },
        {
            "name": "Gaal Dornick",
            "aliases": ["Gaal", "Dornick"],
            "confidence": 0.96,
            "role": "supporting",
            "first_mention": "Seldon's young protégé"
        }
    ]
    print(json.dumps(expected_output, indent=2))
    
    print("\n" + "=" * 60)
    print("\nAdvantages over traditional NLP:")
    print("✓ Automatically merged aliases (Hari, Seldon, Hari Seldon)")
    print("✓ Identified roles (protagonist vs supporting)")
    print("✓ Filtered out generic titles unless specific (filtered 'Grand Vizier')")
    print("✓ Understood context (Emperor = Cleon I, not a generic title)")
    print("✓ Provided confidence scores for each extraction")
    
    print("\n" + "=" * 60)
    print("\nNote: This is a demonstration script.")
    print("Actual LLM calls require API keys and internet connection.")
    print("For production use, implement error handling and rate limiting.")
