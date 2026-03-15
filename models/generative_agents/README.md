# Generative Agents — Mesa-LLM Skeleton

A minimal implementation of the [Generative Agents](https://arxiv.org/abs/2304.03442) (Park et al., 2023) architecture using mesa-llm.

## What this is

Three agents live in a small town:
- **Maria** — cafe owner, warm, chatty, knows everyone
- **James** — novelist, introverted, observant, moved here for quiet
- **Lily** — college student, new in town, trying to make friends

Each step, agents observe their surroundings, plan actions through chain-of-thought reasoning, move around or talk to neighbors, and periodically reflect on their experiences. Social dynamics emerge from the interaction of personas, memory, and proximity.

## How it maps to the paper

| Paper Component | Mesa-LLM Primitive | Notes |
|---|---|---|
| Observation | `LLMAgent.generate_obs()` | Builds self_state + local_state from grid neighbors |
| Planning | `CoTReasoning.plan()` | Structured chain-of-thought → tool call execution |
| Memory Stream | `STLTMemory` | Short-term buffer + LLM-summarized long-term memory |
| Reflection | `GenerativeAgent._reflect()` | Direct LLM call to synthesize recent memory into insights |
| Action | `apply_plan()` → `move_one_step`, `speak_to` | Built-in mesa-llm tools for movement and communication |

## What a full implementation would add

- **Retrieval-based memory** — score memories by recency × importance × relevance (Section 4.2 of the paper)
- **Reflection trees** — synthesize observations into higher-level insights, triggered by importance thresholds
- **Hourly schedule planning** — recursive decomposition from day plan → hour blocks → 5-minute actions
- **Spatial awareness** — named locations (cafe, park, library) instead of raw grid coordinates
- **Multi-day simulation** — day/night cycles with sleep, morning planning, evening reflection

## Running

```bash
# With Ollama (default: llama3.2)
python model.py

# With a specific model and step count
python model.py ollama/gemma3:4b 6

# With OpenAI
python model.py openai/gpt-4o-mini 4
```

## mesa-llm findings from building this

1. **Reflection requires bypassing the reasoning system** — `self.reasoning.plan()` always injects tool schemas and forces a tool call via `tool_choice="required"`. For pure text generation (like reflection), you have to call `self.llm.generate(prompt=...)` directly. Same workaround as the `llm_wealth_distribution` model.

2. **STLTMemory as a proxy for the memory stream** — the paper's memory stream scores every observation by recency, importance, and relevance. Mesa-llm's STLTMemory only does recency (FIFO buffer) + summarization. A production implementation would need a custom Memory subclass with vector similarity retrieval.

3. **`selected_tools=[]` bug still affects this model** — without the fix from PR #[TBD], agents that should only reflect or observe still get movement/teleport tools injected. The fix (changing `if selected_tools:` to `if selected_tools is not None:`) resolves this.

4. **Per-agent LLM client creation** — each of the 3 agents + their STLTMemory creates a separate LLM client (6 total for 3 agents). For Ollama this means 6 model load warnings. Related to issue #200.

5. **Ollama produces string-encoded JSON for tool arguments** — when Ollama calls `teleport_to_location`, it sends `"[1, 2]"` (a string) instead of `[1, 2]` (an actual list). This causes `too many values to unpack` when mesa-llm tries to use it as coordinates. Same issue with `speak_to` — `listener_agents_unique_ids` arrives as a string, so the `in` operator fails. The model still runs because errors are caught and the simulation continues, but tool actions silently fail. Related to issue #173 (JSON validation).