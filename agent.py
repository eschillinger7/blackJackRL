# from tensorflow.keras.optimizers import Adam
from game import *
import gym
from gym import spaces
import random
from model import policy, update_Q_values, showQ

# from tensorflow import *
# import numpy as np
# from tensorflow.keras.models import Sequential, Model
# from tensorflow.keras.layers import Dense, Flatten, Input

# import tensorflow.keras
# KERAS_VERSION = tensorflow.keras.__version__


class blackJackEnv(gym.Env):
    def __init__(self):
        super(blackJackEnv, self).__init__()
        self.action_space = spaces.Discrete(2)  # Hit or Stand
        self.observation_space = spaces.Tuple((
            spaces.Discrete(32),
            spaces.Discrete(11),
            spaces.Discrete(2)
        ))
        self.epsilon = 0.1
        self.reset()

    def reset(self):
        self.c = cards()
        self.p = player(self.c)
        self.d = dealer(self.c)
        self.state = self.get_obs()
        return self.state

    def step(self, action):
        if action == 1:  # Hit
            self.p.hit()
            self.state = self.get_obs()
            if self.p.bust():
                reward = -1
                done = True
            else:
                reward = 0
                done = False
        else:  # Stand
            if self.d.total == 21:
                reward = -1
            while self.d.total < 17:
                self.d.hit()
            done = True
            if self.d.bust() or self.p.total > self.d.total:
                reward = 1
            elif self.p.total == self.d.total:
                reward = .5
            else:
                reward = -1
            self.state = self.get_obs()
        return self.state, reward, done, {}

    def get_obs(self):
        return (self.p.total, self.d.getVal(self.d.hand[0]), int(self.p.aces > 0))


def train(episodes):
    env = blackJackEnv()
    won = 0
    tied = 0
    for episode in range(episodes):
        obs = env.reset()
        print(obs)
        done = False
        while not done:
            action = policy(obs, .2)
            next_obs, reward, done, _ = env.step(action)
            update_Q_values(obs, action, reward,
                            next_obs, done)
            obs = next_obs
        if reward == 1:
            won += 1
        if reward == .5:
            tied += 1


def play(episodes):
    won = 0
    tied = 0

    for episode in range(episodes):
        print("Episode #", episode+1)
        env = blackJackEnv()
        obs = env.reset()
        done = False

        while not done:
            action = policy(obs, .0)
            print("Observation: ", obs)
            if action == 1:
                print("Hit")
            else:
                print("Stay")
            next_obs, reward, done, _ = env.step(action)
            update_Q_values(obs, action, reward,
                            next_obs, done)
            obs = next_obs
            if reward == 1:
                won += 1
            if reward == .5:
                tied += 1
        print("Player hand: ", env.p.hand, "Player total: ", env.p.total)
        print("Dealer hand: ", env.d.hand, "Dealer total: ", env.d.total)

        print("\n\n\n")

    print("Percentage won: ", won/episodes)
    print("Percentage tied: ", tied/episodes)
    print("Percentage lost: ", (episodes-won-tied)/episodes)
    showQ()


def main():
    # episodes = 10
    # for episode in range(1, episodes+1):
    #     env = blackJackEnv()
    #     obs = env.reset()
    #     done = False

    #     while not done:
    #         action = policy()  # Random action for now
    #         obs, reward, done, _ = env.step(action)
    #     print("Episode: ", "Final reward: ", reward)
    train(5000)
    play(1000)


if __name__ == "__main__":
    main()
