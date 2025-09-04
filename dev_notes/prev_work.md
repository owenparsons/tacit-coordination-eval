# LLM coordination

**Coordination Games with Observable History**: Your benchmark is closest to work on coordination games where agents can observe previous rounds but cannot directly communicate. This falls under the category of "repeated coordination games with observable actions."

**Target Sum Games**: The specific mechanic of agents contributing numbers to reach a target sum is reminiscent of:
- **Public goods games** (where agents contribute to a shared resource)
- **Volunteer's dilemma** variations (where coordination is needed to achieve a threshold)
- **Coordination games with continuous action spaces** (since agents choose from a range rather than discrete options)

## LLM-Specific 'no communication' papers:
1. **"Strategic Communication and Language Bias in Multi-Agent LLM Coordination" (2024)**: Explores whether allowing agents to communicate amplifies language-driven effects, with experiments conducted both with and without communication

2. **"LLM-Coordination: Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language Models" (2023)**: Analyzes LLMs in Pure Coordination Settings where agents must cooperate to maximize gains through Agentic Coordination tasks

### Classical game theory literature on 'no communication':
- **Pure Coordination Games** (Schelling, 1960) - The foundational work on coordination without communication
- **"The Strategy of Conflict"** by Thomas Schelling - Introduces focal points and tacit coordination
- **Common Knowledge and Coordination** (Lewis, 1969) - Philosophical foundations
- **"Games and Decisions"** by Luce & Raiffa - Mathematical treatment of non-cooperative games
- **Evolutionary Game Theory** literature (Maynard Smith, Weibull) - How coordination emerges without communication

### Experimental economics on 'silent coordination':
- **Van Huyck, Battalio & Beil (1990)** - Laboratory coordination games without communication
- **Mehta, Starmer & Sugden (1994)** - Focal points in pure coordination games
- **Crawford, Gneezy & Rottenstreich (2008)** - The power of focal points

## Literature on 'observable history' games

### Repeated games with observable actions:
- **Folk Theorem Literature** (Fudenberg & Maskin, 1986) - How cooperation emerges in repeated games
- **"A Theory of Repeated Games"** by Mailath & Samuelson - Comprehensive treatment
- **Kandori & Matsushima (1998)** - Private observation in repeated games
- **"The Evolution of Cooperation"** by Axelrod - Tournament studies with observable history

### LLM studies with history/memory:
- **Multi-round negotiation benchmarks** that show previous interactions
- **Repeated prisoner's dilemma with LLMs** (various 2023-2024 papers)
- **Sequential decision-making studies** in multi-agent settings

### Experimental work on history effects:
- **Camera & Casari (2009)** - Cooperation with and without communication in public goods
- **Fehr & Gächter (2000)** - Cooperation and punishment with observable contributions
- **Dal Bó (2005)** - Cooperation in infinitely repeated games

## Game theory concepts

### Keynesian Beauty Contest

A Keynesian beauty contest is a beauty contest in which judges are rewarded for selecting the most popular faces among all judges, rather than those they may personally find the most attractive. In game theory, this translates to:

**The Game**: Participants guess a number between 0 to 100 and the participant whose guess was closest to 2/3rd of the average of all guesses would win.

**Nash Equilibrium**: The Nash equilibrium of this game will be 0 because if every one chooses 0, the 2/3rd of the average will be 0 and everyone will be a winner.

**Strategic Logic**: If the average play was any number N, then the optimal choice is to pick a number 2/3 of N, with upper bound of 67 for initial reasoning.

**Applications**: Applied to stock markets, it suggests that investors profit more by anticipating popular stocks, rather than those with intrinsic value.

### Coordination games with payoff uncertainty

These are games where:
- Players must coordinate actions but don't know the exact payoff structure
- Uncertainty about other players' preferences or the game's rewards
- Players must make decisions based on incomplete information about consequences
- Often studied in mechanism design and contract theory
- Examples include: coordination under incomplete information about state of the world, games with private types, coordination with unknown network effects

### Threshold public goods games

These games involve:
- **Structure**: Multiple agents can contribute to a public good
- **Threshold**: The good is only provided if total contributions reach a minimum threshold
- **Payoff**: Everyone benefits if threshold is met, regardless of individual contribution
- **Strategic Problem**: Free-rider problem vs. coordination problem
- **Examples**: Funding a public project, environmental collective action, crowdfunding
- **Key Papers**: Palfrey & Rosenthal (1984), Croson & Marks (2000)
