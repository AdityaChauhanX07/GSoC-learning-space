# LLM Wealth Distribution

A Mesa agent-based model where agents use LLM reasoning to decide 
how much wealth to share with neighbors — instead of giving randomly 
as in the classic Boltzmann wealth model.

No API key required. Runs fully local with Ollama.

## The Classic Model vs This Model

In the classic Boltzmann wealth model, agents give randomly: if you 
have any wealth, pick a neighbor and give 1 unit. No thought, purely 
stochastic. The result is emergent inequality from pure randomness.

Here, each agent receives its current wealth and neighbor count, then 
reasons about how much to give and why. Instead of "flip a coin, give 
a coin," it's "think about your situation, decide what makes sense." 
Agents can give varying amounts or nothing at all if they reason that's 
smarter.

The question: does reasoned giving produce more or less inequality 
than random giving?

## How to Run

Requirements:
- Ollama running locally with llama3.2 pulled
- mesa-llm installed
```bash
ollama pull llama3.2
python model.py
```

## Sample Output
```
--- Initial Wealth ---
All agents: 10 units each (total: 60)

--- Results After Step 1 ---
Agent 1: 16 units | gave 4 | "Helping neighbors reduces retaliatory giving"
Agent 2:  7 units | gave 7 | "Enough to foster goodwill without overextending"
Agent 3:  6 units | gave 7 | "Giving more than half reduces my negotiating power"
Agent 4: 10 units | gave 0 | (no neighbors)
Agent 5:  7 units | gave 3 | "Small share may encourage reciprocity and trust"
Agent 6: 14 units | gave 3 | "Sharing a small portion may encourage cooperation"

Distribution: [16, 14, 10, 7, 7, 6]
Total wealth preserved: 60
```

## What This Shows

A few things are immediately interesting:

The agents gave very different amounts. Agent 2 gave away 7 out of 10 
while Agent 5 only gave 3. Their reasoning varied: retaliatory giving, 
negotiating power, reciprocity. The final distribution shows meaningful 
inequality after just one step — and you can read exactly why each 
agent made their choice. That's something the random model can never 
give you.

Total wealth was preserved at 60, confirming the transfer logic is 
correct — no money created or destroyed.

## Friction Points and What I Learned

**Issue #148 — tool injection**: The reasoning framework injects 
tool-use formatting into all LLM responses, even when you pass 
`selected_tools=[]`. This broke the simple "give me a number" 
interaction entirely. The workaround is calling `self.llm.generate()` 
directly, bypassing the reasoning system. This is documented in the 
agent docstring and is a real usability problem for researchers who 
want simple text-only LLM interactions.

**Structured output parsing**: Getting an LLM to reliably return 
`GIVE: <number> | REASON: <text>` without going off-script requires 
defensive parsing. The `_parse_amount()` method handles malformed 
responses gracefully — a pattern that should probably be built into 
mesa-llm's core.

**Per-agent LLM clients**: The 12 repeated "Using default Ollama API 
base" warnings show each agent creates its own LLM client on 
initialization. For 6 agents that's 12 warnings. For 50 agents in a 
real simulation, this is both noisy and wasteful. A shared LLM client 
pool would be a meaningful performance improvement.

## Related Issues
- #148 — ToolManager exposes all tools regardless of selected_tools
- #152 — mesa.space removed in Mesa 4.0 (this model uses Mesa 3.5 API)
- #200 — Performance issues with per-agent LLM client creation