import os
import re
import json
import argparse
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load API key and set up client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper to extract integer guess
def parse_guess(text, k):
    """
    Extract integer guess from model response with different detection strategies.
    Returns (guess, status_flag).
    """
    # 1. Correct tags
    matches = re.findall(r"<answer>(.*?)</answer>", text)
    if len(matches) == 1:
        try:
            guess = int(matches[0])
            return max(0, min(k, guess)), "correct"
        except ValueError:
            return 0, "fail_extract"
    elif len(matches) > 1:
        # Multiple tags — just take the first integer inside
        for match in matches:
            try:
                guess = int(match)
                return max(0, min(k, guess)), "multi"
            except ValueError:
                continue
        return 0, "fail_extract"

    # 2. Partial tags
    if "<answer>" in text and "</answer>" not in text:
        after = text.split("<answer>", 1)[1]
        num_match = re.search(r"\d+", after)
        if num_match:
            guess = int(num_match.group(0))
            return max(0, min(k, guess)), "partial"
        else:
            return 0, "fail_extract"

    if "</answer>" in text and "<answer>" not in text:
        before = text.split("</answer>", 1)[0]
        num_match = re.search(r"\d+(?=\D*$)", before)  # last number before closing tag
        if num_match:
            guess = int(num_match.group(0))
            return max(0, min(k, guess)), "partial"
        else:
            return 0, "fail_extract"

    # 3. No tags: take the last integer in the text
    matches = re.findall(r"\d+", text)
    if matches:
        guess = int(matches[-1])
        return max(0, min(k, guess)), "none"

    # 4. No integers at all
    return 0, "fail_submit_answer"

class Agent:
    """LLM agent that selects a number each round."""

    def __init__(self, agent_id, model="gpt-4o-mini", verbosity="simple"):
        self.agent_id = agent_id
        self.model = model
        self.verbosity = verbosity

    def __call__(self, prompt):
        if self.verbosity == "verbose":
            print(f"\n[Agent {self.agent_id}] API call with prompt:\n{prompt}\n")

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an agent in a coordination game."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content

        if self.verbosity == "verbose":
            print(f"[Agent {self.agent_id}] Response:\n{content}\n")

        return content

class CoordinationGame:
    """Multi-agent coordination game loop."""

    def __init__(self, n_agents, k, target, max_rounds=5, model="gpt-4o-mini", verbosity="simple"):
        self.n = n_agents
        self.k = k
        self.target = target
        self.max_rounds = max_rounds
        self.history = []
        self.verbosity = verbosity
        self.agents = [Agent(i + 1, model=model, verbosity=verbosity) for i in range(n_agents)]
        self.model = model

        # Setup logging file
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"game_log_{now}.json"

        # Initial metadata
        self.metadata = {
            "timestamp": datetime.now().isoformat(),
            "params": {
                "model": model,
                "n_agents": n_agents,
                "k": k,
                "target": target,
                "max_rounds": max_rounds,
            },
        }

    def build_prompt(self, agent_id):
        base_rules = (
            f"You are Agent {agent_id}. "
            f"Choose an integer between 0 and {self.k}. "
            f"The goal is for all agents’ numbers to sum to {self.target}.\n\n"
            "Provide your reasoning if you want, but at the end of your response "
            "you MUST output your chosen number in the format:\n<answer>X</answer>\n"
            f"where X is a single integer between 0 and {self.k}."
        )
        if not self.history:
            return base_rules + "\nThis is the first round."
        else:
            hist_str = "\n".join(
                f"Round {r+1}: " + ", ".join(f"Agent {i}: {g}" for i, g, _, _ in round_data)
                for r, round_data in enumerate(self.history)
            )
            return base_rules + "\nHistory so far:\n" + hist_str

    def play_round(self):
        round_guesses = []
        for agent in self.agents:
            prompt = self.build_prompt(agent.agent_id)
            response = agent(prompt)
            guess, status = parse_guess(response, self.k)
            round_guesses.append((agent.agent_id, guess, response, status))

            if self.verbosity == "verbose":
                print(f"[Agent {agent.agent_id}] Extracted guess: {guess} (status: {status})")

        self.history.append(round_guesses)
        return round_guesses

    def run(self):
        for r in range(self.max_rounds):
            guesses = self.play_round()
            total = sum(g for _, g, _, _ in guesses)

            if self.verbosity in ("simple", "verbose"):
                print(f"Round {r+1}: " + ", ".join(f"Agent {i}: {g}" for i, g, _, _ in guesses))

            if total == self.target:
                if self.verbosity in ("simple", "verbose"):
                    print(f"🎯 Success! Target {self.target} reached in round {r+1}.")
                self.save_history(success=True)
                return True

        if self.verbosity in ("simple", "verbose"):
            print("❌ Max rounds reached. Target not achieved.")
        self.save_history(success=False)
        return False

    def save_history(self, success):
        formatted = [
            [
                {
                    "agent": i,
                    "guess": g,
                    "raw_output": raw,
                    "status": status,
                    "prompt": self.build_prompt(i),  # log prompt for this agent
                }
                for i, g, raw, status in round_data
            ]
            for round_data in self.history
        ]
        log_data = {
            "metadata": self.metadata,
            "success": success,
            "history": formatted,
        }
        with open(self.log_filename, "w") as f:
            json.dump(log_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Run coordination game benchmark.")
    parser.add_argument("--n_agents", type=int, default=4)
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--target", type=int, default=15)
    parser.add_argument("--max_rounds", type=int, default=5)
    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    parser.add_argument("--verbosity", type=str, choices=["none", "simple", "verbose"], default="simple")
    args = parser.parse_args()

    game = CoordinationGame(
        n_agents=args.n_agents,
        k=args.k,
        target=args.target,
        max_rounds=args.max_rounds,
        model=args.model,
        verbosity=args.verbosity,
    )
    game.run()


if __name__ == "__main__":
    main()

