
# Tacit coordination evaluation

A benchmark for evaluating Large Language Model (LLM) coordination abilities through multi-agent target-sum games without direct communication. This evaluation framework tests how well LLMs can collaborate to achieve shared goals when they can only observe previous actions but cannot communicate directly.

### The task

Multiple LLM agents (n) are tasked with selecting numbers from a specified range (0 to k) such that their collective sum equals a target value (t). Agents receive the complete history of previous rounds, showing each agent's past choices, but cannot communicate or strategize together. Success requires emergent coordination through pattern recognition, strategic reasoning, and adaptive behavior.

### Features

- Customizable parameters (number of agents, value range, target sum) for systematic evaluation
- Agents see all previous rounds but cannot communicate
- Handles LLM output validation and numerical extraction
- Records all agent responsesin logs

### Research significance

This benchmark addresses a gap in multi-agent LLM evaluation by focusing on pure coordination without communication channels. Unlike existing benchmarks that either allow communication or use simple binary choices, this evaluation tests sophisticated coordination abilities through:

- Strategic adaptation based on observed patterns
- Implicit role allocation among agents  
- Convergence toward optimal collective behavior
- Robustness across different parameter configurations

### Applications

The benchmark provides insights relevant to AI safety, multi-agent systems deployment, and understanding emergent coordination in LLMs. Results can inform the design of AI systems that must coordinate in environments with limited communication, such as distributed computing, autonomous vehicle coordination, or collaborative problem-solving scenarios.

---

## Setup

### Prerequisites
- [uv](https://github.com/astral-sh/uv) for managing dependencies and running the project  
- An OpenAI API key (store it in a `.env` file as `OPENAI_API_KEY="your_key_here"`)  

### Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/tacit-coordination-eval.git
cd tacit-coordination-eval
uv sync
```

This will create a `.venv` folder and install required packages.

### Running the Benchmark
You can run the coordination game using:

```bash
uv run main.py
```

By default, this will run with 4 agents, each choosing numbers between 0–10, with a target sum of 15 and a maximum of 5 rounds.

### Parameters
You can customize the benchmark with command-line arguments:

| Argument        | Default       | Description |
|-----------------|---------------|-------------|
| `--n_agents`    | 4             | Number of LLM agents |
| `--k`           | 10            | Upper bound of number range (0 to k) |
| `--target`      | 15            | Target sum the agents must reach |
| `--max_rounds`  | 5             | Maximum number of rounds before termination |
| `--model`       | gpt-4o-mini   | OpenAI model to use for agents |
| `--verbosity`   | simple        | Output mode: `none`, `simple`, or `verbose` |

Example:

```bash
uv run main.py --n_agents 3 --k 8 --target 20 --max_rounds 10 --verbosity verbose
```

This runs with 3 agents, numbers 0–8, target sum of 20, max 10 rounds, and verbose logging.

### Output & Logging
- Logs are automatically saved in `game_log_YYYYMMDD_HHMMSS.json`  
- Each log includes:
  - Experiment metadata (model, params, timestamp)  
  - Full prompts sent to agents  
  - Raw responses from each agent  
  - Extracted guesses and parsing status  
  - Whether the target was achieved  


