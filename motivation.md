# Motivation

## Who I am

I'm a freshman at Rhodes College in Memphis, Tennessee studying Mathematics and Computer Science. Most of my programming experience is in Python, specifically building things with LLM APIs. I've worked with OpenAI, Anthropic, and Ollama, and I've built a handful of projects that go beyond basic chat - stuff like an LLM auditing system that detects stale claims (Temporal Blindspot), an autonomous computer operator using vision-based agents (Phantom Dev), and a financial decision engine that combines Monte Carlo simulations with LLM-written reports (Golden Scout).

I'm comfortable with async Python from building FastAPI backends, and I've spent a lot of time dealing with the messy reality of getting LLMs to produce reliable structured output.

## Why Mesa

I found Mesa through the GSoC organizations list, but what got me interested was mesa-llm specifically. Every LLM project I've built has the same hard problem: the LLM call itself is easy, but making the output reliable enough to drive downstream logic is where everything breaks. Mesa-llm is trying to solve exactly that - putting LLMs inside a simulation framework where their outputs actually have to work, not just sound good.

When I set it up locally and started building models, I realized how much work there is to do. The test suite doesn't pass on Mesa 4.0 at all. The tool system injects tools even when you explicitly opt out. Ollama support is rough. These aren't abstract problems I read about in the issues list - I hit every one of them in my first two days of building.

## What I want to learn

I want to get better at maintaining real open source software. I've built a lot of solo projects but I haven't worked on something where other people depend on the code being stable, well-tested, and backwards compatible. Mesa-llm is small enough that I can understand the whole codebase but real enough that the problems matter.

I'm also interested in the agent-based modeling side. The Generative Agents paper is what convinced me this intersection of LLMs and ABM is worth investing in. Building my skeleton implementation showed me how much of the paper's architecture is missing from mesa-llm and what it would take to close that gap.

## Where I want to go

I want to get mesa-llm to a point where a researcher can install it, run a model with Ollama, and have it just work. Right now that's not the case. The immediate goal is the GSoC project - Mesa 4.0 compatibility, fixing the core bugs I've found, making Ollama a first-class citizen, and writing examples that actually help new users.

Longer term, I'm a freshman, so I have three more years at Rhodes. I'd like to stay involved with Mesa after GSoC ends. The Generative Agents skeleton I built is something I want to turn into a full implementation, and there's a lot of room to build better memory systems, better tool validation, and better examples based on real research papers.