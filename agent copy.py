# from tensorflow.keras.optimizers import Adam
from game import *
import gym
from gym import spaces
import random

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
            while self.d.total < 17:
                self.d.hit()
            done = True
            if self.d.bust() or self.p.total > self.d.total:
                reward = 1
            elif self.p.total == self.d.total:
                reward = 0
            else:
                reward = -1
        return self.state, reward, done, {}

    def get_obs(self):
        return (self.p.total, self.d.hand[0], int(self.p.aces > 0))


# def build_model(states, actions):
#     inputs = Input(shape=(states,))
#     x = Dense(24, activation='relu')(inputs)
#     x = Dense(24, activation='relu')(x)
#     outputs = Dense(actions, activation='linear')(x)
#     model = Model(inputs=inputs, outputs=outputs)
#     return model


# def build_model(states, actions):
#     inputs = Input(shape=(states,))
#     x = Dense(24, activation='relu')(inputs)
#     x = Dense(24, activation='relu')(x)
#     outputs = Dense(actions, activation='linear')(x)
#     model = Model(inputs=inputs, outputs=outputs)
#     return model


# def main():
#     env = blackJackEnv()
#     action = env.action_space.n
#     states = env.observation_space.spaces[0].n
#     model = build_model(states, action)
#     model.summary()

#     model.compile(optimizer=Adam(lr=1e-3), loss='mse')


def main():
    episodes = 10
    for episode in range(1, episodes+1):
        env = blackJackEnv()
        obs = env.reset()
        print()
        done = False

        while not done:
            action = env.action_space.sample()  # Random action for now
            obs, reward, done, _ = env.step(action)
        print("Episode: ", "Final reward: ", reward)

    # env = blackJackEnv()
    # # print("Observation Space:", env.observation_space)
    # # print("Observation Space Shape:", env.observation_space.shape[0])

    # action = env.action_space.n
    # states = env.observation_space.spaces[0].n
    # model = build_model(states, action)
    # model.summary()

    # dqn = build_agent(model, action)
    # dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    # dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)


if __name__ == "__main__":
    main()
