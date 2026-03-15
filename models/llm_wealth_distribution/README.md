# LLM Wealth Distribution

Agents use LLM reasoning to decide how much wealth to share with neighbors, instead of giving randomly like in the classic Boltzmann wealth model.

Runs fully local with Ollama, no API key needed.

## Classic model vs this one

In the classic Boltzmann wealth model, if you have any money, you pick a random neighbor and give them 1 unit. No thinking involved, just randomness. The interesting result is that inequality emerges from pure chance.

This model changes the giving rule. Each agent gets told its current wealth and how many neighbors it has, then reasons about how much to give and why. Agents can give different amounts or nothing at all if they think that's the better move.

The question: does reasoned giving produce more or less inequality than random giving?

## How to run

```bash
ollama pull llama3.2
python model.py
```

## Sample output

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

## What's interesting here

The agents gave very different amounts. Agent 2 gave away 7 out of 10, Agent 5 only gave 3. Their reasoning varied: retaliatory giving, negotiating power, reciprocity. You get meaningful inequality after just one step, and you can read exactly why each agent made their choice. The random model can never give you that.

Total wealth stayed at 60, so the transfer logic is correct. No money created or destroyed.

## What I learned building this

**Issue #148 hit me again.** The reasoning framework injects tool schemas into all LLM responses, even when you pass `selected_tools=[]`. This broke my simple "give me a number" interaction completely. I had to call `self.llm.generate()` directly, bypassing the reasoning system. Same workaround as the hello_llm_agent model. This is a real usability problem for anyone who wants simple text-only LLM interactions.

**Structured output parsing is hard.** Getting an LLM to reliably return `GIVE: <number> | REASON: <text>` without going off-script requires defensive parsing. My `_parse_amount()` method handles malformed responses gracefully. This pattern should probably be built into mesa-llm's core.

**Per-agent LLM clients are noisy.** The 12 repeated "Using default Ollama API base" warnings come from each agent creating its own LLM client on init. 6 agents = 12 warnings (agent + memory each get a client). For 50 agents in a real simulation this would be both noisy and wasteful. A shared client pool would help.

## Related issues
- #148 - ToolManager exposes all tools regardless of selected_tools
- #152 - mesa.space removed in Mesa 4.0 (this model uses Mesa 3.5 API)
- #200 - Performance issues with per-agent LLM client creation