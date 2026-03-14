import mesa
from agents import GreeterAgent


class HelloModel(mesa.Model):
    """
    Minimal mesa-llm model using local Ollama.
    No API key required.

    Known limitations discovered during development:
    - selected_tools=[] does not prevent tool injection (issue #148)
    - Out-of-bounds coordinates not validated (issue #198)
    - Mesa 4.0 breaks this model entirely (issue #152)
    """

    def __init__(self, n_agents=2, llm_model="ollama/llama3.2"):
        super().__init__()
        self.grid = mesa.space.MultiGrid(5, 5, torus=False)

        for _ in range(n_agents):
            agent = GreeterAgent(
                model=self,
                llm_model=llm_model,
                system_prompt=(
                    "You are a friendly agent in a simulation. "
                    "Always respond in plain text. Never use tools."
                ),
            )
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        self.agents.shuffle_do("step")


if __name__ == "__main__":
    print("Running Hello LLM Agent with local Ollama (llama3.2)...")
    print("No API key required.\n")

    model = HelloModel(n_agents=2)
    model.step()

    print("\n--- Results ---")
    for agent in model.agents:
        print(f"Agent {agent.unique_id}: {agent.greeting}")