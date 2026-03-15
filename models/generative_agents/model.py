"""
Generative Agents — Model

3 agents in a 5x5 town grid:
- Maria (cafe owner) — warm, chatty, knows everyone
- James (writer) — introverted, observant, working on a novel
- Lily (college student) — curious, energetic, new in town

The model runs for a few steps. Agents observe their surroundings,
plan actions via CoT reasoning, talk to neighbors, and periodically
reflect on their experiences. Social dynamics emerge from the
interaction of personas + memory + proximity.
"""

from mesa.model import Model
from mesa.space import MultiGrid
from rich import print

from agents import GenerativeAgent

# --- Agent Personas ---
# Inspired by the Smallville characters in Park et al., 2023.
# Each has a name, backstory, daily routine, and personality traits.

PERSONAS = [
    {
        "name": "Maria",
        "persona": (
            "You own the town's only cafe, 'Morning Grounds.' "
            "You've lived here for 20 years and know everyone. "
            "You love gossip but mean well."
        ),
        "daily_routine": (
            "Open cafe at dawn, serve regulars, chat with customers, "
            "restock supplies in the afternoon, close up in the evening."
        ),
        "traits": ["warm", "talkative", "nosy", "generous"],
    },
    {
        "name": "James",
        "persona": (
            "You're a novelist who moved to this small town for quiet. "
            "You're working on a mystery novel and find the townspeople "
            "interesting as character inspiration."
        ),
        "daily_routine": (
            "Write in the morning, take a walk at midday, visit the cafe "
            "for coffee in the afternoon, read in the evening."
        ),
        "traits": ["introverted", "observant", "thoughtful", "private"],
    },
    {
        "name": "Lily",
        "persona": (
            "You're a college student who just moved here for a summer "
            "internship. You don't know anyone yet and are trying to "
            "make friends and learn about the town."
        ),
        "daily_routine": (
            "Internship work in the morning, explore the town at midday, "
            "study in the afternoon, look for social events in the evening."
        ),
        "traits": ["curious", "energetic", "friendly", "anxious"],
    },
]


class GenerativeAgentsModel(Model):
    """
    Skeleton of the Generative Agents sandbox environment.

    Maps the paper's architecture to mesa-llm primitives:
    - Observation → LLMAgent.generate_obs() (builds self_state + local_state)
    - Planning → CoTReasoning.plan() (structured chain-of-thought → tool call)
    - Memory → STLTMemory (short-term buffer + LLM-summarized long-term)
    - Reflection → GenerativeAgent._reflect() (periodic memory synthesis)
    - Action → apply_plan() (execute tool calls: move, speak_to)

    What the full version would add:
    - Hourly schedule decomposition (plan → sub-plan → minute-level)
    - Memory retrieval scoring (recency × importance × relevance)
    - Reflection trees with importance thresholds
    - Spatial map with named locations (cafe, park, library)
    """

    def __init__(
        self,
        llm_model: str = "ollama/llama3.2",
        width: int = 5,
        height: int = 5,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.grid = MultiGrid(width, height, torus=False)

        # Create agents from personas
        positions = [(1, 1), (3, 3), (2, 4)]  # spread them out
        for persona_data, pos in zip(PERSONAS, positions):
            agent = GenerativeAgent(
                model=self,
                llm_model=llm_model,
                **persona_data,
            )
            self.grid.place_agent(agent, pos)

    def step(self):
        print(
            f"\n[bold purple]═══ Step {self.steps} "
            f"═══════════════════════════════════════════[/bold purple]"
        )
        self.agents.shuffle_do("step")

    def print_summary(self):
        """Print a summary of each agent's reflections after the simulation."""
        print("\n[bold cyan]═══ Simulation Summary ═══[/bold cyan]")
        for agent in self.agents:
            print(f"\n[bold]{agent.name}[/bold] (Agent {agent.unique_id}):")
            if agent.reflections:
                for i, r in enumerate(agent.reflections, 1):
                    print(f"  Reflection {i}: {r}")
            else:
                print("  No reflections yet.")


# ── Run without graphics ──
if __name__ == "__main__":
    import sys

    llm = sys.argv[1] if len(sys.argv) > 1 else "ollama/llama3.2"
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    print(f"[bold]Running Generative Agents skeleton with {llm} for {steps} steps[/bold]\n")

    model = GenerativeAgentsModel(llm_model=llm)
    for _ in range(steps):
        model.step()

    model.print_summary()