# Aditya Chauhan - Mesa GSoC Learning Space

GSoC 2026 candidate | Applying for **Mesa-LLM iteration to production**
Rhodes College, Memphis TN | GitHub: [@AdityaChauhanX07](https://github.com/AdityaChauhanX07)

## About Me

I'm a freshman at Rhodes College studying Mathematics and Computer Science. I've built several LLM-powered systems using OpenAI, Anthropic, and Ollama APIs, with strong async Python experience from FastAPI backends and concurrent LLM orchestration.

I'm applying to push mesa-llm from experimental to production-ready - making it stable, well-tested, Mesa 4.0 compatible, and usable for researchers who don't want to deal with cloud API keys just to try it out.

## What I've Built

| Model | What it does | What I found |
|-------|-------------|--------------|
| [hello_llm_agent](models/hello_llm_agent/) | Two agents on a grid decide whether to say hello using Ollama | Discovered `selected_tools=[]` bug (#148) - tools get injected even when you explicitly pass an empty list |
| [llm_wealth_distribution](models/llm_wealth_distribution/) | Agents reason about how much wealth to share instead of giving randomly | Had to bypass the reasoning system entirely to get text responses. Per-agent LLM clients create noisy warnings (#200) |
| [generative_agents](models/generative_agents/) | Skeleton of [Generative Agents](https://arxiv.org/abs/2304.03442) (Park et al., 2023) mapped to mesa-llm primitives | STLTMemory is only a rough proxy for the paper's memory stream. Ollama sends string-encoded JSON that breaks tool calls (#173) |

## Contributions

**PR submitted:** [fix: selected_tools=[] should return no tools, not all tools](https://github.com/projectmesa/mesa-llm/pull/XXX) - one-line fix in `ToolManager.get_all_tools_schema()`, changing `if selected_tools:` to `if selected_tools is not None:` so that an empty list actually means "no tools" instead of "all tools."

**Peer reviews:**
- [PR #153](https://github.com/projectmesa/mesa-llm/pull/153) - flagged that Mesa 4.0 compat was tested against source, not the official pre-release
- [PR #195](https://github.com/projectmesa/mesa-llm/pull/195) - validated `model.time` as correct public API since Mesa 3.4, flagged `SimpleNamespace` isinstance check coupling production code to test infra
- [PR #378](https://github.com/mesa/mesa-examples/pull/378) (mesa-examples) - found that LLM reasoning is never actually called in the Prisoner's Dilemma model, decisions are hardcoded to "cooperate"

## Technical Findings

These all came from actually building models and running tests, not just reading code.

**Mesa 4.0 compatibility is completely broken.** I installed the official pre-release (`pip install --pre mesa`) and ran the test suite. Result: 0 tests collected, immediate `ModuleNotFoundError: No module named 'mesa.space'`. Mesa 4.0 removed `mesa.space` entirely. Full details in [notes/mesa4_compatibility_findings.md](notes/mesa4_compatibility_findings.md).

**The reasoning system can't do text-only responses.** `self.reasoning.plan()` always injects tool schemas and sets `tool_choice="required"`. If you want the LLM to just return text (like "give 3 coins" or a reflection), you have to bypass the reasoning system and call `self.llm.generate()` directly. I hit this in all three models.

**selected_tools=[] is broken (#148).** Passing an empty list should mean "no tools." Instead it returns all tools because `[]` is falsy in Python. I submitted a PR fixing this.

**Ollama's tool calling produces bad JSON (#173).** Ollama sends `"[1, 2]"` (a string) instead of `[1, 2]` (an actual list) for tool arguments. This breaks `teleport_to_location` and `speak_to` with type errors. The simulation keeps running because errors are caught, but tool actions silently fail.

**Per-agent LLM clients are wasteful (#200).** Each agent plus its STLTMemory creates a separate LLM client. 3 agents = 6 clients = 6 "Using default Ollama API base" warnings at startup. For larger simulations this is both noisy and slow.

**Default LLM assumes you have a Gemini key.** The default model is `gemini/gemini-2.0-flash`. New users who just want to try mesa-llm with Ollama hit an error immediately. The onboarding experience could be a lot better.

## Mesa 4.0 Test Results

On Mesa 3.5.0: **275 passed, 0 failed, 24 warnings** (all `seed` -> `rng` deprecation warnings)

On Mesa 4.0.0a0: **0 tests collected** - complete import failure

Raw output: [mesa4_test_results.txt](mesa4_test_results.txt)

## Links
- [Mesa-LLM repo](https://github.com/projectmesa/mesa-llm)
- [My GitHub](https://github.com/AdityaChauhanX07)