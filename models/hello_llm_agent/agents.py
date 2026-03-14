import mesa
from mesa_llm.llm_agent import LLMAgent
from mesa_llm.reasoning.cot import CoTReasoning


class GreeterAgent(LLMAgent):
    """
    A minimal LLM agent that decides how to greet neighbors.
    Uses local Ollama model — no API key required.
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

    def step(self):
        obs = self.generate_obs()

        neighbor_count = len(obs.local_state)
        prompt = (
            f"You are agent {self.unique_id} on a grid. "
            f"You can see {neighbor_count} neighbors. "
            f"Decide: should you say hello or stay quiet? "
            f"Respond with just your decision and a one-sentence reason."
        )

        plan = self.reasoning.plan(prompt=prompt, obs=obs, selected_tools=[])
        self.greeting = str(plan)