"""
Generative Agents (Park et al., 2023) — Mesa-LLM Skeleton

A minimal implementation of the Generative Agents architecture using mesa-llm.
3 agents in a small town: a cafe owner, a writer, and a student.
Each agent has a daily routine, can observe neighbors, form opinions, 
and initiate conversations — the core loop from the paper.

Paper: https://arxiv.org/abs/2304.03442

What this skeleton demonstrates:
- Observation → Planning → Action loop (Section 4 of the paper)
- Memory-informed reasoning via mesa-llm's STLTMemory
- Agent-to-agent communication via speak_to tool
- Emergent social behavior from simple persona prompts
- Bypasses tool injection bug (#148) using direct LLM calls for reflection

What a full implementation would add:
- Retrieval-based memory (recency × importance × relevance scoring)
- Reflection trees (synthesizing memories into higher-level insights)
- Hourly schedule planning with recursive decomposition
- Spatial awareness (rooms, buildings, paths)
"""

from mesa_llm.llm_agent import LLMAgent
from mesa_llm.reasoning.cot import CoTReasoning


class GenerativeAgent(LLMAgent):
    """
    A generative agent inspired by Park et al., 2023.

    Each agent has:
    - A persona (name, occupation, traits, daily routine)
    - Short-term + long-term memory via STLTMemory
    - CoT reasoning for planning actions
    - A reflection step that synthesizes recent experience
    """

    def __init__(
        self,
        model,
        llm_model,
        name: str,
        persona: str,
        daily_routine: str,
        traits: list[str],
        vision: int = 2,
    ):
        system_prompt = (
            f"You are {name}. {persona}\n"
            f"Your typical daily routine: {daily_routine}\n"
            f"Your personality traits: {', '.join(traits)}.\n"
            "You live in a small town. You can see and talk to nearby people. "
            "Act naturally based on your persona — make small talk, go about "
            "your routine, and form opinions about the people you meet."
        )

        super().__init__(
            model=model,
            reasoning=CoTReasoning,
            llm_model=llm_model,
            system_prompt=system_prompt,
            vision=vision,
            internal_state=[f"name: {name}"] + [f"trait: {t}" for t in traits],
            step_prompt=None,  # we provide prompts dynamically
        )

        self.name = name
        self.persona = persona
        self.daily_routine = daily_routine
        self.traits = traits
        self.reflections = []  # stores reflection strings across steps

    def _get_time_of_day(self) -> str:
        """Map simulation step to a rough time of day."""
        step = self.model.steps
        hours = ["morning", "midday", "afternoon", "evening", "night"]
        return hours[step % len(hours)]

    def _reflect(self) -> str:
        """
        Generate a reflection on recent experiences.

        This is the simplified version of the paper's reflection mechanism.
        The full version would score memories by recency × importance × relevance
        and generate higher-level insights. Here we just ask the LLM to
        synthesize recent short-term memory into a one-sentence takeaway.

        Uses direct LLM call to bypass the reasoning system's tool injection
        (issue #148 workaround — same approach as llm_wealth_distribution model).
        """
        recent_memory = self.memory.format_short_term()
        if recent_memory == "No recent memory.":
            return ""

        prompt = (
            f"You are {self.name}. Based on your recent experiences:\n"
            f"{recent_memory}\n\n"
            "In one sentence, what is your main takeaway or reflection? "
            "Focus on what you learned about the people around you or your situation."
        )

        response = self.llm.generate(prompt=prompt)
        reflection = response.choices[0].message.content.strip()
        self.reflections.append(reflection)
        return reflection

    def step(self):
        time_of_day = self._get_time_of_day()

        # Build a context-aware prompt
        reflection_context = ""
        if self.reflections:
            latest = self.reflections[-1]
            reflection_context = f"\nYour most recent reflection: {latest}\n"

        prompt = (
            f"It is {time_of_day} in the small town. "
            f"You are {self.name}. {self.persona}\n"
            f"{reflection_context}"
            f"Based on your routine ({self.daily_routine}), "
            f"what do you do now? If someone is nearby, you might talk to them. "
            f"Otherwise, go about your day.\n"
            "Decide: move somewhere, talk to a neighbor, or continue your activity."
        )

        # Plan and act
        observation = self.generate_obs()
        plan = self.reasoning.plan(prompt=prompt, obs=observation)
        self.apply_plan(plan)

        # Reflect every 2 steps (paper does it on importance threshold)
        if self.model.steps > 0 and self.model.steps % 2 == 0:
            self._reflect()