# Hello LLM Agent

A minimal mesa-llm model using local Ollama. No API key needed.

## What it does

Two agents sit on a 5x5 grid. Each step, they look around and use an LLM (llama3.2 via Ollama) to decide whether to say hello or stay quiet. That's it. I built this as the simplest possible mesa-llm model to understand how the framework works before doing anything complex.

## How to run

You need Ollama running locally with llama3.2 pulled:
```bash
ollama pull llama3.2
```

Then from this directory:
```bash
python model.py
```

## What I found

### selected_tools=[] doesn't work (issue #148)

This was the big one. I passed `selected_tools=[]` and added a system prompt saying "Never use tools." The idea was to get pure text responses, no tool calls. But the agents still called `teleport_to_location` instead of just saying hello.

The root cause is in `ToolManager.get_all_tools_schema()` - it checks `if selected_tools:`, and in Python an empty list is falsy. So `[]` gets treated the same as `None` and all tools get injected anyway. I ended up submitting a fix for this as a PR.

### Mesa 4.0 breaks everything

Running with Mesa 4.0.0a0 gives an immediate import error: `ModuleNotFoundError: No module named 'mesa.space'`. Mesa 4.0 removed `mesa.space` entirely. Full findings in [notes/mesa4_compatibility_findings.md](../../notes/mesa4_compatibility_findings.md).

### Ollama silently does the wrong thing

Models without function calling support (like gemma3:4b) don't warn you that they can't handle tools. They just produce garbage tool calls. llama3.2 supports function calling but still ignores the `selected_tools` constraint since the bug is on mesa-llm's side, not Ollama's.

## Related issues
- #148 - ToolManager exposes all tools regardless of selected_tools
- #152 - mesa.space removed in Mesa 4.0
- #198 - Out-of-bounds coordinates not validated