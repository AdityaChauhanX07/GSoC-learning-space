from mesa_llm.llm_agent import LLMAgent
from mesa_llm.reasoning.cot import CoTReasoning


class WealthAgent(LLMAgent):
    """
    A wealth agent that uses LLM reasoning to decide
    whether and how much to give to a random neighbor.

    Unlike the classic Boltzmann model where giving is random,
    this agent reasons about its own wealth level and the
    neighbor's situation before deciding.

    Note: Uses self.llm.generate() directly instead of
    self.reasoning.plan() to bypass tool injection (issue #148).
    """

    def __init__(self, model, llm_model, initial_wealth=10):
        super().__init__(
            model=model,
            reasoning=CoTReasoning,
            llm_model=llm_model,
            system_prompt=(
                "You are an agent in an economic simulation. "
                "You make decisions about sharing wealth with neighbors. "
                "Always respond in plain text only. Never use tools. "
                "Be concise — one decision and one short reason."
            ),
            vision=1,
        )
        self.wealth = initial_wealth
        self.decision = None
        self.amount_given = 0

    def step(self):
        if self.wealth == 0:
            self.decision = "stay quiet (no wealth to give)"
            return

        obs = self.generate_obs()
        neighbor_count = len(obs.local_state)

        if neighbor_count == 0:
            self.decision = "stay quiet (no neighbors)"
            return

        prompt = (
            f"You are agent {self.unique_id} in an economic simulation.\n"
            f"Your current wealth: {self.wealth} units.\n"
            f"You have {neighbor_count} neighbor(s) nearby.\n"
            f"Decide how much to give (0 to {self.wealth}).\n"
            f"Reply ONLY in this format, nothing else:\n"
            f"GIVE: <number> | REASON: <one sentence>"
        )

        response = self.llm.generate(prompt=prompt)

        if response and response.choices:
            content = response.choices[0].message.content
            if content:
                self.decision = content.strip()
                amount = self._parse_amount(content)
                self._give_wealth(amount)
            else:
                self.decision = "[empty response]"
        else:
            self.decision = "[no response]"

    def _parse_amount(self, text: str) -> int:
        """Parse GIVE: <number> from LLM response."""
        try:
            if "GIVE:" in text:
                give_part = text.split("GIVE:")[1].split("|")[0].strip()
                amount = int(give_part)
                return max(0, min(amount, self.wealth))
        except (ValueError, IndexError):
            pass
        return 0

    def _give_wealth(self, amount: int):
        """Give wealth to a random neighbor."""
        if amount <= 0 or self.wealth < amount:
            self.amount_given = 0
            return

        neighbors = list(self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        ))

        if not neighbors:
            self.amount_given = 0
            return

        recipient = self.random.choice(neighbors)
        self.wealth -= amount
        recipient.wealth += amount
        self.amount_given = amount