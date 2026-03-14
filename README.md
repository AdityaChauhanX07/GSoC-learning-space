# Aditya Chauhan — Mesa GSoC Learning Space

GSoC 2026 candidate | Applying for **Mesa-LLM iteration to production**  
Rhodes College, Memphis TN | GitHub: [@AdityaChauhanX07](https://github.com/AdityaChauhanX07)

## About Me

I'm a student at Rhodes College with hands-on experience building
LLM-powered applications using OpenAI, Anthropic, and Ollama APIs.
I have strong async Python skills and have built several AI projects
including personality modeling systems and financial data extraction tools.

I'm applying to push mesa-llm from experimental to production-ready —
making it stable, well-tested, Mesa 4.0 compatible, and accessible
to researchers who want LLM agents without needing cloud API keys.

## Models Built

| Model | Description | Key Learning |
|-------|-------------|--------------|
| [hello_llm_agent](models/hello_llm_agent/) | Minimal Ollama-based LLM agent on a grid | Discovered #148, silent tool injection bug |

## What I've Learned So Far

### From building hello_llm_agent (March 14, 2026)
- mesa-llm silently degrades when Ollama models lack function calling support
- `selected_tools=[]` does not prevent default tool injection (issue #148)
- Out-of-bounds LLM-generated coordinates are not validated
- The default LLM is hardcoded to Gemini — friction for new users without API keys

### From reading the codebase
- `llm_agent.py` mixes Mesa 3 and Mesa 4 spatial APIs in the same file
- 24 deprecation warnings in the test suite (`seed` → `rng`) signal Mesa 4.0 migration debt
- All 3 existing examples are complex — no simple starter model exists
- Memory (STLTMemory) is always-on and not optional for simple use cases

## My GSoC Proposal Focus

**Mesa-LLM iteration to production (350 hours)**

Core priorities based on actual codebase experience:
1. Mesa 4.0 compatibility — fix mixed API imports, migrate spatial layer
2. Core bug fixes — async path issues, tool injection, JSON validation
3. Ollama-first experience — better local inference support and docs
4. Simple examples — a "hello world" that works out of the box

## Links
- [My GSoC Proposal](coming March 16)
- [Mesa-LLM repo](https://github.com/projectmesa/mesa-llm)
- [My GitHub](https://github.com/AdityaChauhanX07)
- [Matrix intro](https://matrix.to/#/#mesa-gsoc:matrix.org)