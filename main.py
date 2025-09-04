import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API key and set up client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper to extract integer guess
def parse_guess(text, k):
    """Extract the first integer guess from the model output."""
    match = re.search(r"\d+", text)
    if match:
        guess = int(match.group(0))
        return max(0, min(k, guess))  # clip to range [0, k]
    return 0  # fallback if invalid

class Agent:
    """LLM agent that selects a number each round."""

    def __init__(self, agent_id, model="gpt-4o-mini"):
        self.agent_id = agent_id
        self.model = model

    def __call__(self, prompt):
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an agent in a coordination game."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class CoordinationGame:
    """Multi-agent coordination game loop."""

    def __init__(self, n_agents, k, target, max_rounds=10, model="gpt-4o-mini"):
        self.n = n_agents
        self.k = k
        self.target = target
        self.max_rounds = max_rounds
        self.history = []
        self.agents = [Agent(i + 1, model=model) for i in range(n_agents)]

    def build_prompt(self, agent_id):
        base_rules = (
            f"You are Agent {agent_id}. "
            f"Choose an integer between 0 and {self.k}. "
            f"The goal is for all agents’ numbers to sum to {self.target}."
        )
        if not self.history:
            return base_rules + "\nThis is the first round."
        else:
            hist_str = "\n".join(
                f"Round {r+1}: " + ", ".join(f"Agent {i}: {g}" for i, g, _ in round_data)
                for r, round_data in enumerate(self.history)
            )
            return base_rules + "\nHistory so far:\n" + hist_str

    def play_round(self):
        round_guesses = []
        for agent in self.agents:
            prompt = self.build_prompt(agent.agent_id)
            response = agent(prompt)
            guess = parse_guess(response, self.k)
            round_guesses.append((agent.agent_id, guess, response))
        self.history.append(round_guesses)
        return round_guesses

    def run(self):
        for r in range(self.max_rounds):
            guesses = self.play_round()
            total = sum(g for _, g, _ in guesses)
            print(f"Round {r+1}: " + ", ".join(f"Agent {i}: {g}" for i, g, _ in guesses))
            if total == self.target:
                print(f"🎯 Success! Target {self.target} reached in round {r+1}.")
                return True
        print("❌ Max rounds reached. Target not achieved.")
        return False

    def save_history(self, filename="game_log.json"):
        formatted = [
            [{"agent": i, "guess": g, "raw_output": raw} for i, g, raw in round_data]
            for round_data in self.history
        ]
        with open(filename, "w") as f:
            json.dump(formatted, f, indent=2)

def main():
    game = CoordinationGame(n_agents=4, k=5, target=15, max_rounds=10, model="gpt-4o-mini")
    game.run()
    game.save_history("run_logs/coordination_game_log.json")


if __name__ == "__main__":
    main()

