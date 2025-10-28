# plot_results.py
import csv
import matplotlib.pyplot as plt

csv_path = "sarsa_training_log.csv"
episodes, steps, returns, epsilons = [], [], [], []

with open(csv_path, newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        episodes.append(int(row["episode"]))
        steps.append(int(row["steps"]))
        returns.append(float(row["return"]))
        epsilons.append(float(row["epsilon"]))

# Courbe des retours
plt.figure()
plt.plot(episodes, returns)
plt.xlabel("Episode")
plt.ylabel("Return (R)")
plt.title("SARSA – Return per Episode")
plt.tight_layout()
plt.savefig("return_per_episode.png")

# Courbe des steps
plt.figure()
plt.plot(episodes, steps)
plt.xlabel("Episode")
plt.ylabel("Steps survived")
plt.title("SARSA – Steps per Episode")
plt.tight_layout()
plt.savefig("steps_per_episode.png")

# Courbe epsilon
plt.figure()
plt.plot(episodes, epsilons)
plt.xlabel("Episode")
plt.ylabel("Epsilon")
plt.title("Epsilon decay")
plt.tight_layout()
plt.savefig("epsilon_decay.png")

print("Plots saved: return_per_episode.png, steps_per_episode.png, epsilon_decay.png")
