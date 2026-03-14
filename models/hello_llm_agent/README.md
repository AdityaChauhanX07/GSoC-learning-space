# Hello LLM Agent

A minimal mesa-llm model demonstrating a local Ollama agent.
No API key required.

## What I learned building this

1. **gemma3:4b doesn't support function calling** — mesa-llm 
   silently degrades with no clear error message. New users will 
   be confused. Better model validation or docs needed.

2. **Default tools inject even with selected_tools=[]** — 
   ToolManager registers default tools at the class level, so 
   passing an empty list doesn't prevent tool injection. 
   Related to issue #148.

3. **Out-of-bounds coordinates not caught** — LLM generated 
   (3,7) on a 5x5 grid. No validation error raised.

## How to run

Requirements: Ollama running locally with llama3.2 pulled.
```bash
ollama pull llama3.2
python model.py
```