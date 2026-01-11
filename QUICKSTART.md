# Quick Start Guide: Using LLMs for Character Analysis

## Option 1: Quick Comparison (No API Keys Required)

Run the comparison notebook to see how LLMs compare to traditional NLP:

```bash
jupyter notebook LLM_vs_Traditional_Comparison.ipynb
```

This notebook uses simulated LLM responses to demonstrate the differences without requiring API keys.

## Option 2: Using the LLM Character Extractor

### Prerequisites

1. Install required packages:
```bash
pip install nltk pandas
pip install openai  # or anthropic, or ollama
```

2. Set up your API key (choose one):

**For OpenAI:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**For Anthropic:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**For Ollama (local, free):**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2  # or another model
# No API key needed!
```

### Basic Usage

```python
from llm_character_extractor import LLMCharacterAnalyzer

# Read your text
with open('Foundation.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Initialize analyzer (choose your provider)
analyzer = LLMCharacterAnalyzer(
    provider='openai',  # or 'anthropic' or 'ollama'
    model='gpt-4',      # or 'claude-3-opus' or 'llama2'
)

# Extract characters
characters = analyzer.extract_characters(text)

# Print results
for char in characters:
    print(f"{char['name']}: {char['role']} (confidence: {char['confidence']})")
    print(f"  Aliases: {', '.join(char['aliases'])}")
    print()

# Analyze relationships
character_names = [c['name'] for c in characters]
relationships = analyzer.analyze_relationships(text, character_names)

# Print relationships
for rel in relationships['relationships']:
    print(f"{rel['character1']} ← {rel['type']} → {rel['character2']}")
    print(f"  Strength: {rel['strength']}/10")
    print()
```

## Option 3: Free Local LLM with Ollama

**Advantages:**
- ✅ Completely free
- ✅ No API keys required
- ✅ Works offline
- ✅ Privacy-preserving (data never leaves your machine)

**Setup:**

1. Install Ollama: https://ollama.ai

2. Pull a model:
```bash
ollama pull llama2
# or for better results:
ollama pull mixtral
ollama pull llama2:70b
```

3. Use with the analyzer:
```python
from llm_character_extractor import LLMCharacterAnalyzer

analyzer = LLMCharacterAnalyzer(
    provider='ollama',
    model='llama2'  # or 'mixtral'
)

characters = analyzer.extract_characters(text)
```

## Performance & Cost Comparison

| Provider | Model | Speed | Cost (per novel) | Quality |
|----------|-------|-------|------------------|---------|
| OpenAI | GPT-4 | Fast | ~$2-5 | Excellent |
| OpenAI | GPT-3.5 | Very Fast | ~$0.50-1 | Good |
| Anthropic | Claude-3-Opus | Fast | ~$3-6 | Excellent |
| Anthropic | Claude-3-Sonnet | Fast | ~$1-3 | Very Good |
| Ollama | Llama2 (7B) | Medium | $0 (Free) | Good |
| Ollama | Mixtral (8x7B) | Slow | $0 (Free) | Very Good |

## Tips for Best Results

1. **Chunk long texts**: For texts over 10,000 words, process in chunks
2. **Use GPT-4 or Claude-3-Opus for best quality**: Worth the cost for important analysis
3. **Use Ollama for experimentation**: Free and privacy-preserving
4. **Validate results**: Always review character lists, especially for critical work
5. **Use hybrid approach**: LLM for curation, traditional NLP for metrics

## Example Workflow

```python
# 1. Use LLM to get clean character list
analyzer = LLMCharacterAnalyzer(provider='ollama', model='mixtral')
llm_characters = analyzer.extract_characters(full_text)

# 2. Extract just the main names
character_list = [c['name'] for c in llm_characters if c['role'] != 'minor']

# 3. Use traditional NLP for quantitative analysis
from nltk_character_analysis import analyze_interactions
interactions = analyze_interactions(full_text, character_list)

# 4. Use LLM for deep-dive on key relationships
key_relationships = analyzer.analyze_relationships(
    full_text, 
    character_list[:5]  # Top 5 characters
)

# Best of both worlds: Accuracy + Speed + Rich insights
```

## Troubleshooting

### "LLM response is not valid JSON"
- Solution: Increase temperature parameter to 0.1-0.3
- Solution: Add retry logic (LLMs occasionally fail)

### "API rate limit exceeded"
- Solution: Add delays between requests
- Solution: Use smaller chunks
- Solution: Switch to local Ollama

### "Costs are too high"
- Solution: Use GPT-3.5 instead of GPT-4
- Solution: Use Ollama (free)
- Solution: Only analyze key sections, not full text

### "Results not reproducible"
- Solution: Set temperature=0 for more deterministic outputs
- Solution: Use seed parameter if available
- Solution: For critical work, consider traditional NLP

## Further Reading

- [LLM_CHARACTER_ANALYSIS.md](LLM_CHARACTER_ANALYSIS.md) - Detailed comparison
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Ollama Documentation](https://github.com/ollama/ollama)
