from mesa_llm.llm_agent import LLMAgent
from mesa_llm.reasoning.cot import CoTReasoning


class GreeterAgent(LLMAgent):
    """
    A minimal LLM agent that decides how to greet neighbors.
    Uses local Ollama model — no API key required.

    Demonstrates: basic LLM reasoning in a Mesa simulation.
    Known issue: selected_tools=[] does not prevent tool injection
    in mesa-llm 0.3.0 (issue #148). Workaround: system prompt
    explicitly instructs text-only response.
    """

    def __init__(self, model, llm_model, system_prompt):
        super().__init__(
            model=model,
            reasoning=CoTReasoning,
            llm_model=llm_model,
            system_prompt=system_prompt,
            vision=1,
        )
        self.greeting = None
        self.reasoning_text = None

    def step(self):
        obs = self.generate_obs()
        neighbor_count = len(obs.local_state)

        prompt = (
            f"You are agent {self.unique_id} on a grid. "
            f"You can see {neighbor_count} neighbor(s). "
            f"Decide: should you say hello or stay quiet? "
            f"Reply in plain text only. Do not use any tools. "
            f"Format: DECISION: <hello or quiet> | REASON: <one sentence>"
        )

        plan = self.reasoning.plan(
            prompt=prompt,
            obs=obs,
            selected_tools=[],
        )

        # Extract text content from plan
        if hasattr(plan, "llm_plan") and plan.llm_plan is not None:
            content = getattr(plan.llm_plan, "content", None)
            if content:
                self.greeting = content
            else:
                # LLM used a tool call instead of text — issue #148
                self.greeting = f"[tool call instead of text — see issue #148]"
        else:
            self.greeting = "[no response]"