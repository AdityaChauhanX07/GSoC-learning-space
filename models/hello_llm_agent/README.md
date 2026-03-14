# Hello LLM Agent

A minimal mesa-llm model demonstrating a local Ollama LLM agent.
No API key required — runs fully offline.

## What this model does

Two agents are placed on a 5x5 grid. Each step, they observe
their surroundings and use an LLM (running locally via Ollama)
to decide how to respond to neighbors.

## How to run

Requirements:
- Ollama installed and running locally
- llama3.2 pulled: `ollama pull llama3.2`
- mesa-llm installed: `pip install -e ".[dev]"` from mesa-llm root
```bash
python model.py
```

## What I learned building this

1. **gemma3:4b doesn't support function calling** — mesa-llm
   silently degrades with no clear error message. New users
   hitting this will be confused. Better model validation or
   clearer error output is needed.

2. **Default tools inject even with selected_tools=[]** — 
   ToolManager registers default tools at the class level.
   Passing an empty list to selected_tools doesn't prevent
   tool injection into the LLM prompt. Related to issue #148.

3. **Out-of-bounds coordinates not caught** — LLM generated
   position (3,7) on a 5x5 grid (valid range 0-4). No 
   validation error was raised, the move silently failed.

4. **Plan content is None when tools are called** — When the
   LLM responds with a tool call instead of text, the plan
   content field is None. Makes debugging harder for new users.

## Related issues
- #148 — ToolManager exposes all tools regardless of agent state
- #198 — ContinuousSpace boundary check allows out-of-bounds moves
- #182 — Tutorial should mention Ollama must be running