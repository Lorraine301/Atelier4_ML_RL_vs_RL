import pygame
import agent as ag
import game as g
import numpy as np
import matplotlib.pyplot as plt

class GameLearning:

    def __init__(self, alpha=0.7, gamma=0.95, eps=0.1):

        # deux agents RL
        self.agent1 = ag.Qlearning(alpha, gamma, eps)
        self.agent2 = ag.Qlearning(alpha, gamma, eps)

        self.game = g.Game(self.agent1, self.agent2, mode="RL_RL")

    def train(self, episodes=2000):
        rewards1, rewards2 = [], []

        for ep in range(episodes):
            r1, r2 = self.game.play(training=True, render=False)
            rewards1.append(sum(r1))
            rewards2.append(sum(r2))

        return rewards1, rewards2

def plot_learning_curves(r1, r2):
    plt.figure(figsize=(10,5))

    plt.plot(r1, alpha=0.3, label="Agent RL 1")
    plt.plot(r2, alpha=0.3, label="Agent RL 2")

    window = 50
    plt.plot(np.convolve(r1, np.ones(window)/window, mode="valid"),
             label="Agent 1 Moving Avg", linewidth=2)
    plt.plot(np.convolve(r2, np.ones(window)/window, mode="valid"),
             label="Agent 2 Moving Avg", linewidth=2)

    plt.xlabel("Episodes")
    plt.ylabel("Total Reward")
    plt.title("RL vs RL – Learning Curves")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    pygame.init()

    gl = GameLearning()

    print("Entraînement RL vs RL...")
    r1, r2 = gl.train(episodes=2000)

    plot_learning_curves(r1, r2)
    
    # TEST RL vs RL
    print("Test final visuel RL vs RL(sans apprentissage)")
    test_r1, test_r2 = gl.game.play(
    training=False,
    render=True,
    steps=2000
)
    
    # SCORE FINAL
    score_agent1 = sum(test_r1)
    score_agent2 = sum(test_r2)

    print("\n===== SCORE FINAL =====")
    print(f"Agent RL 1 : {score_agent1}")
    print(f"Agent RL 2 : {score_agent2}")

    pygame.quit()
