import numpy as np
import os
import pickle
import collections
import random

class Qlearning:
    """
     class for Q-learning .
    Parameters
    ----------
    alpha : float
        learning rate
    gamma : float
        temporal discounting rate
    eps : float
        probability of random action vs. greedy action
    eps_decay : float
        epsilon decay rate. Larger value = more decay
    """

    def __init__(self, alpha, gamma, eps, eps_decay=0):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay

        # Q-table
        self.actions = [-1, 0, 1]   # up, stay, down
        self.Q = collections.defaultdict(lambda: np.zeros(len(self.actions)))

    #Le choix d’action Greedy   
    def get_action(self, s):
        """ 
        Greedy policy (ε-greedy)
        
        """
        if random.random() < self.eps:
            return random.choice(self.actions)
        else:
            return self.actions[np.argmax(self.Q[s])]

    def update(self, s, s_, a, a_, r):
        """
        Perform the Q-Learning update of Q values.
        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """
        #La mise à jour de Qlearning
        """
        Q-learning update
        """
        a_idx = self.actions.index(a)
        best_next = np.max(self.Q[s_])

        self.Q[s][a_idx] += self.alpha * (
            r + self.gamma * best_next - self.Q[s][a_idx]
        )
        # decay epsilon
        self.eps = max(0.01, self.eps - self.eps_decay)