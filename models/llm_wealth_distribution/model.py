import mesa
from agents import WealthAgent


class WealthModel(mesa.Model):
    """
    LLM Wealth Distribution model.

    Agents reason about whether to give wealth to neighbors,
    instead of giving randomly as in the classic Boltzmann model.

    Research question: does reasoned giving produce more or less
    inequality than random giving?
    """

    def __init__(
        self,
        n_agents=5,
        initial_wealth=10,
        llm_model="ollama/llama3.2",
        width=5,
        height=5,
    ):
        super().__init__()
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.n_agents = n_agents

        for _ in range(n_agents):
            agent = WealthAgent(
                model=self,
                llm_model=llm_model,
                initial_wealth=initial_wealth,
            )
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        self.agents.shuffle_do("step")

    def wealth_stats(self):
        """Return basic wealth distribution stats."""
        wealths = [a.wealth for a in self.agents]
        total = sum(wealths)
        max_w = max(wealths)
        min_w = min(wealths)
        avg = total / len(wealths)
        return {
            "total": total,
            "max": max_w,
            "min": min_w,
            "avg": round(avg, 2),
            "distribution": sorted(wealths, reverse=True),
        }


if __name__ == "__main__":
    print("LLM Wealth Distribution Model")
    print("Agents reason about giving — not random")
    print("Using local Ollama (llama3.2) — no API key needed\n")

    model = WealthModel(n_agents=6, initial_wealth=10)

    print("--- Initial Wealth ---")
    for agent in model.agents:
        print(f"Agent {agent.unique_id}: {agent.wealth} units")

    print("\n--- Running Step 1 ---\n")
    model.step()

    print("\n--- Results ---")
    for agent in model.agents:
        print(f"Agent {agent.unique_id}: {agent.wealth} units | "
              f"gave {agent.amount_given} | decision: {agent.decision}")

    stats = model.wealth_stats()
    print(f"\n--- Wealth Stats ---")
    print(f"Distribution: {stats['distribution']}")
    print(f"Max: {stats['max']} | Min: {stats['min']} | "
              f"Avg: {stats['avg']}")
    print(f"Total wealth preserved: {stats['total']} "
              f"(started with {6 * 10})")