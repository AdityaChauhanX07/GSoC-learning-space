# Hello LLM Agent

A minimal mesa-llm model using local Ollama. No API key required.

## What this model does

Two agents are placed on a 5x5 grid. Each step, they observe their 
surroundings and use an LLM to decide whether to say hello or stay quiet.

## How to run

Requirements:
- Ollama running locally with llama3.2: `ollama pull llama3.2`
- mesa-llm installed: `pip install -e ".[dev]"` from mesa-llm root
```bash
python model.py
```

## What I learned building this

### Bug confirmed: issue #148
`selected_tools=[]` does not prevent tool injection in mesa-llm 0.3.0.
Even with an explicit system prompt saying "Never use tools" and passing
an empty selected_tools list, the ToolManager still exposes default tools
to the LLM. The agent ignores the constraint and calls tools instead of
responding in text.

This means researchers cannot build simple text-reasoning agents without
working around the tool system entirely. The fix requires changes to
ToolManager to actually respect the selected_tools parameter.

### Mesa 4.0 breaks this model
Running with Mesa 4.0.0a0 produces an immediate ImportError:
`ModuleNotFoundError: No module named 'mesa.space'`
Full findings in: [notes/mesa4_compatibility_findings.md](../../notes/mesa4_compatibility_findings.md)

### Silent Ollama degradation
Models without function calling support (gemma3:4b) produce no warning —
they just silently call wrong tools. llama3.2 supports function calling
but still ignores the selected_tools constraint.

## Related issues
- #148 — ToolManager exposes all tools regardless of selected_tools
- #152 — mesa.space removed in Mesa 4.0
- #198 — Out-of-bounds coordinates not validated