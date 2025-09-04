
# Tacit coordination evaluation

A benchmark for evaluating Large Language Model (LLM) coordination abilities through multi-agent target-sum games without direct communication. This evaluation framework tests how well LLMs can collaborate to achieve shared goals when they can only observe previous actions but cannot communicate directly.

### The task

Multiple LLM agents (n) are tasked with selecting numbers from a specified range (0 to k) such that their collective sum equals a target value (t). Agents receive the complete history of previous rounds, showing each agent's past choices, but cannot communicate or strategize together. Success requires emergent coordination through pattern recognition, strategic reasoning, and adaptive behavior.

### Features

- **Parametric Design**: Fully customizable parameters (number of agents, value range, target sum) for systematic evaluation
- **Observable History**: Agents see all previous rounds but cannot communicate
- **Robust Parsing**: Handles LLM output validation and numerical extraction
- **Comprehensive Logging**: Records all agent responses for detailed analysis
- **Flexible Framework**: Compatible with Inspect AI or standalone implementation

### Research significance

This benchmark addresses a gap in multi-agent LLM evaluation by focusing on pure coordination without communication channels. Unlike existing benchmarks that either allow communication or use simple binary choices, this evaluation tests sophisticated coordination abilities through:

- Strategic adaptation based on observed patterns
- Implicit role allocation among agents  
- Convergence toward optimal collective behavior
- Robustness across different parameter configurations

### Applications

The benchmark provides insights relevant to AI safety, multi-agent systems deployment, and understanding emergent coordination in LLMs. Results can inform the design of AI systems that must coordinate in environments with limited communication, such as distributed computing, autonomous vehicle coordination, or collaborative problem-solving scenarios.