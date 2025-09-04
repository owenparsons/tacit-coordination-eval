from math import comb, ceil, log
import matplotlib.pyplot as plt
import numpy as np

def single_round_probability(n, k, t):
    """
    Probability that sum of n agents' guesses (0..k) equals t in a single round.
    """
    p = 0
    max_i = t // (k + 1)
    for i in range(max_i + 1):
        sign = (-1) ** i
        numerator = comb(n, i) * comb(t - i*(k+1) + n - 1, n - 1) if t - i*(k+1) + n - 1 >= 0 else 0
        p += sign * numerator
    total_combinations = (k + 1) ** n
    return p / total_combinations

def probability_in_x_rounds(n, k, t, x):
    """
    Probability of hitting the target at least once in x independent rounds.
    """
    p1 = single_round_probability(n, k, t)
    return 1 - (1 - p1) ** x

def rounds_for_target_probability(n, k, t, target_prob):
    """
    Compute minimum number of rounds to reach target probability.
    """
    p1 = single_round_probability(n, k, t)
    if p1 == 0:
        return float('inf')  # impossible
    x = log(1 - target_prob) / log(1 - p1)
    return ceil(x)

def plot_probability_growth(n, k, t, max_rounds=50):
    """
    Generate a simple plot of probability of hitting the target vs. number of rounds.
    """
    x_vals = np.arange(1, max_rounds + 1)
    y_vals = [probability_in_x_rounds(n, k, t, x) for x in x_vals]

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, marker='o')
    plt.title(f"Probability of hitting target sum t={t} over rounds\n(n={n}, k={k})")
    plt.xlabel("Number of rounds")
    plt.ylabel("Probability of hitting target at least once")
    plt.grid(True)
    plt.ylim(0, 1.05)
    plt.show()