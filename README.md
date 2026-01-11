# Foundation-Character-Interactions
Data Science analysis of the relationships in the novel Foundation by Isaac Asimov

<img width="1054" alt="FoundationClusters" src="https://user-images.githubusercontent.com/72196131/136686142-6669222d-3c1c-4dec-b5df-e27df6caae77.png">

## 🤖 LLMs for Character Analysis

**Can LLMs do the general NLP work for character analysis?** **YES!** And often better than traditional approaches.

This repository now includes resources comparing traditional NLTK-based NLP with modern LLM approaches:

### 📚 New Resources

- **[LLM_CHARACTER_ANALYSIS.md](LLM_CHARACTER_ANALYSIS.md)** - Comprehensive analysis of LLMs vs traditional NLP for character extraction
- **[llm_character_extractor.py](llm_character_extractor.py)** - Working Python implementation supporting 7 LLM providers: OpenAI, Anthropic, AWS Bedrock, Google Gemini, OpenRouter, Ollama, and llama.cpp
- **[LLM_vs_Traditional_Comparison.ipynb](LLM_vs_Traditional_Comparison.ipynb)** - Interactive Jupyter notebook comparing both approaches
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with setup instructions for all providers

### 🎯 Key Findings

**LLMs Excel At:**
- ✅ Merging character aliases (e.g., "Hari", "Seldon", "Hari Seldon" → one character)
- ✅ Filtering false positives (locations, titles, organizations)
- ✅ Understanding context and relationships
- ✅ Providing semantic analysis (character roles, traits, motivations)
- ✅ Handling complex literary variations

**Traditional NLP Still Wins For:**
- ✅ Large-scale corpus analysis (1000+ books)
- ✅ Reproducible, deterministic results
- ✅ Zero-cost, offline processing
- ✅ Real-time performance requirements

**Recommended: Hybrid Approach**
- Use LLM once for curated character list creation
- Use traditional NLP for bulk quantitative analysis
- Use LLM for deep relationship analysis

See [LLM_CHARACTER_ANALYSIS.md](LLM_CHARACTER_ANALYSIS.md) for detailed comparison and recommendations.

---

## Original Analysis

## Cluster example

Unsurprisingly, Hober Mallow is out by himself.

|    | Name         |   cluster |
|---:|:-------------|----------:|
| 21 | Anacreon     |         0 |
| 14 | Board        |         0 |
| 12 | City         |         0 |
| 20 | Empire       |         0 |
| 15 | Encyclopedia |         0 |
| 17 | Foundation   |         0 |
| 16 | Galactic     |         0 |
| 18 | Galaxy       |         0 |
| 13 | Periphery    |         0 |
| 19 | Terminus     |         0 |
|  3 | Barr         |         1 |
|  8 | Gorov        |         1 |
|  6 | Jael         |         1 |
| 11 | Lee          |         1 |
|  7 | Pirenne      |         1 |
|  4 | Ponyets      |         1 |
| 10 | Sermak       |         1 |
|  0 | Sutt         |         1 |
|  9 | Twer         |         1 |
|  5 | Verisof      |         1 |
| 35 | Commdor      |         2 |
| 39 | Gaal         |         2 |
| 22 | Hardin       |         2 |
| 25 | Seldon       |         2 |
| 29 | Emperor      |         3 |
| 24 | Fara         |         3 |
| 32 | Grand        |         3 |
| 37 | Hari         |         3 |
| 38 | Korell       |         3 |
| 33 | Lepold       |         3 |
| 26 | Lord         |         3 |
| 34 | Master       |         3 |
| 28 | Pherl        |         3 |
| 27 | Salvor       |         3 |
| 36 | Spirit       |         3 |
| 30 | Trantor      |         3 |
| 31 | Wienis       |         3 |
| 23 | Mallow       |         4 |
|  2 | Well         |         5 |
|  1 | Yes          |         5 |
