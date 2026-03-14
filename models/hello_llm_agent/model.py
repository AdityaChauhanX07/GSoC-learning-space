import mesa
from mesa_llm.llm_agent import LLMAgent
from agents import GreeterAgent


class HelloModel(mesa.Model):
    """Minimal model to test a local Ollama LLM agent."""

    def __init__(self, n_agents=2, llm_model="ollama/llama3.2"):
        super().__init__()
        self.grid = mesa.space.MultiGrid(5, 5, torus=False)

        for _ in range(n_agents):
            agent = GreeterAgent(
                model=self,
                llm_model=llm_model,
                system_prompt="You are a friendly agent in a simulation.",
            )
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        self.agents.shuffle_do("step")


if __name__ == "__main__":
    print("Running Hello LLM Model with local Ollama...")
    model = HelloModel(n_agents=2)
    model.step()
    for agent in model.agents:
        print(f"Agent {agent.unique_id} decided: {agent.greeting}")