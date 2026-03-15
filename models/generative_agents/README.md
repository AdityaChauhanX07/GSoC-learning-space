# Generative Agents - Mesa-LLM Skeleton

A skeleton implementation of [Generative Agents](https://arxiv.org/abs/2304.03442) (Park et al., 2023) using mesa-llm. This maps the paper's core architecture onto mesa-llm's existing primitives to see what works, what's missing, and what a full implementation would need.

## What it does

Three agents live in a small town on a 5x5 grid:
- **Maria** - cafe owner, warm, chatty, knows everyone
- **James** - novelist, introverted, observant, moved here for quiet
- **Lily** - college student, new in town, trying to make friends

Each step, agents observe who's nearby, plan their next action through chain-of-thought reasoning, move around or talk to neighbors, and every 2 steps they reflect on recent experiences. The reflections get fed back into future decisions, so agents build up opinions about each other over time.

## How the paper maps to mesa-llm

The Generative Agents paper has three core components: observation, planning, and reflection.

**Observation** maps cleanly to `LLMAgent.generate_obs()`, which builds a self_state (who am I, where am I) and local_state (who's nearby and what are they like).

**Planning** works through `CoTReasoning.plan()`. The agent thinks step-by-step then executes a tool call (move somewhere or talk to someone).

**Memory** uses mesa-llm's `STLTMemory`, which keeps a short-term buffer of recent events and summarizes older ones into long-term memory using the LLM.

**Reflection** is where it gets hacky. The paper has agents synthesize memories into higher-level insights ("Maria seems to know everyone in town, she'd be good to ask about local events"). Mesa-llm doesn't have a reflection primitive, so I call `self.llm.generate()` directly to get the agent to synthesize its recent memory into a one-sentence takeaway. Same bypass workaround as my other two models.

**Action** uses the built-in `move_one_step` and `speak_to` tools through `apply_plan()`.

## What a full version would need

The skeleton is missing a lot of what makes the paper work:
- Retrieval-based memory scoring (recency x importance x relevance) instead of just FIFO
- Reflection trees that trigger based on importance thresholds, not just every N steps
- Hourly schedule planning with recursive decomposition (day plan -> hour blocks -> 5-min actions)
- Named locations (cafe, park, library) instead of raw grid coordinates
- Multi-day simulation with sleep, morning planning, evening reflection

## Running

```bash
# default: ollama/llama3.2, 4 steps
python model.py

# different model and step count
python model.py ollama/gemma3:4b 6

# with OpenAI
python model.py openai/gpt-4o-mini 4
```

## What I found building this

**Reflection needs the reasoning bypass.** `self.reasoning.plan()` always injects tool schemas and forces a tool call via `tool_choice="required"`. For pure text generation like reflection, you have to call `self.llm.generate(prompt=...)` directly. I hit this same wall in both previous models. Mesa-llm really needs a way to do text-only LLM calls through the reasoning system.

**STLTMemory is a rough proxy for the paper's memory stream.** The paper scores every observation by recency, importance, and relevance. STLTMemory only does recency (FIFO buffer) plus LLM summarization of old memories. A real implementation would need a custom Memory subclass with vector similarity retrieval.

**selected_tools=[] bug (issue #148) still bites.** Agents that should only reflect or observe still get movement/teleport tools injected. The fix I submitted (changing `if selected_tools:` to `if selected_tools is not None:` in ToolManager) resolves this.

**Per-agent LLM clients add up fast.** Each of the 3 agents plus their STLTMemory creates a separate LLM client, so that's 6 total for just 3 agents. With Ollama you get 6 model load warnings at startup. Related to issue #200.

**Ollama sends string-encoded JSON for tool arguments.** When Ollama calls `teleport_to_location`, it sends `"[1, 2]"` (a string) instead of `[1, 2]` (an actual list). This causes `too many values to unpack` when mesa-llm tries to use it as coordinates. Same thing with `speak_to` where `listener_agents_unique_ids` arrives as a string, so the `in` operator fails. The model keeps running because errors are caught, but tool actions silently fail. Related to issue #173 (JSON validation).