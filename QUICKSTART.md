# Quick Start Guide: Using LLMs for Character Analysis

## Option 1: Quick Comparison (No API Keys Required)

Run the comparison notebook to see how LLMs compare to traditional NLP:

```bash
jupyter notebook LLM_vs_Traditional_Comparison.ipynb
```

This notebook uses simulated LLM responses to demonstrate the differences without requiring API keys.

## Option 2: Using the LLM Character Extractor

### Supported Providers

The character extractor now supports **7 different LLM providers**:

1. **OpenAI** - GPT-4, GPT-3.5
2. **Anthropic** - Claude 3 (Opus, Sonnet, Haiku)
3. **AWS Bedrock** - Claude, Titan, and other models
4. **Google Gemini** - Gemini Pro, Gemini Flash
5. **OpenRouter** - Unified API for 100+ models
6. **Ollama** - Local, free models (Llama2, Mixtral, etc.)
7. **llama.cpp Server** - Local, free models with llama.cpp

### Prerequisites

1. Install base packages:
```bash
pip install nltk pandas
```

2. Install provider-specific packages (choose one or more):

**For OpenAI:**
```bash
pip install openai
export OPENAI_API_KEY='your-api-key-here'
```

**For Anthropic:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY='your-api-key-here'
```

**For AWS Bedrock:**
```bash
pip install boto3
export AWS_ACCESS_KEY_ID='your-access-key'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
```

**For Google Gemini:**
```bash
pip install google-generativeai
export GEMINI_API_KEY='your-api-key-here'
```

**For OpenRouter:**
```bash
pip install openai
export OPENROUTER_API_KEY='your-api-key-here'
```

**For Ollama (local, free):**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2  # or mixtral, or other models
# No API key needed!
```

**For llama.cpp Server (local, free):**
```bash
pip install requests
# Download and run llama.cpp server:
# ./server -m your-model.gguf --port 8080
export LLAMACPP_BASE_URL='http://localhost:8080'  # optional
```

### Basic Usage

```python
from llm_character_extractor import LLMCharacterAnalyzer

# Read your text
with open('Foundation.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Initialize analyzer (choose your provider)

# OpenAI
analyzer = LLMCharacterAnalyzer(provider='openai', model='gpt-4')

# Anthropic
analyzer = LLMCharacterAnalyzer(provider='anthropic', model='claude-3-opus-20240229')

# AWS Bedrock
analyzer = LLMCharacterAnalyzer(
    provider='bedrock', 
    model='anthropic.claude-3-sonnet-20240229-v1:0',
    region='us-east-1'
)

# Google Gemini
analyzer = LLMCharacterAnalyzer(provider='gemini', model='gemini-pro')

# OpenRouter
analyzer = LLMCharacterAnalyzer(provider='openrouter', model='anthropic/claude-3-opus')

# Ollama
analyzer = LLMCharacterAnalyzer(provider='ollama', model='llama2')

# llama.cpp Server
analyzer = LLMCharacterAnalyzer(
    provider='llamacpp', 
    model='llama2',
    base_url='http://localhost:8080'
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
| AWS Bedrock | Claude-3-Sonnet | Fast | ~$1-3 | Very Good |
| AWS Bedrock | Titan | Very Fast | ~$0.30-0.80 | Good |
| Google Gemini | Gemini Pro | Very Fast | ~$0.10-0.50 | Very Good |
| Google Gemini | Gemini Flash | Ultra Fast | ~$0.05-0.20 | Good |
| OpenRouter | Various | Varies | ~$0.50-5 | Varies |
| Ollama | Llama2 (7B) | Medium | $0 (Free) | Good |
| Ollama | Mixtral (8x7B) | Slow | $0 (Free) | Very Good |
| llama.cpp | Any GGUF | Medium-Slow | $0 (Free) | Varies |

**Note:** 
- Costs are approximate for analyzing a ~65,000 word novel
- Speed depends on hardware for local models (Ollama, llama.cpp)
- Quality varies by model and prompt engineering

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
