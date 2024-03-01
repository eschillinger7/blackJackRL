import random
import numpy as np


# num_states = 32 * 11 * 2  # Total number of possible states
# num_actions = 2  # Hit or Stand
# Q = np.zeros((num_states, num_actions))  # Q-table
Q = np.zeros((32, 12, 2, 2))


def policy(state, epsilon):

    if random.uniform(0, 1) < epsilon:
        # Explore: choose a random action
        return random.randint(0, 1)
    else:
        # Exploit: choose the action with the highest Q-value
        return np.argmax(Q[state[0], state[1], state[2]])


# Update Q-values using Q-learning algorithm


# def update_Q_values(prev_state, action, reward, next_state, done):
#     # Q-learning update rule
#     global Q

#     alpha = 0.2  # Learning rate
#     gamma = 0.8  # Discount factor

#     print("Q-values before update:")
#     print(Q[prev_state])

#     if not done:
#         Q[prev_state[0], prev_state[1], prev_state[2], action] += alpha * \
#             (reward + gamma * np.max(Q[next_state]) - Q[prev_state, action])
#     else:
#         Q[prev_state[0], prev_state[1], prev_state[2],
#             action] += alpha * (reward - Q[prev_state, action])

#     print("Q-values before update:")
#     print(Q[prev_state])


def update_Q_values(prev_state, action, reward, next_state, done):
    global Q

    alpha = 0.1  # Learning rate
    gamma = 0.99  # Discount factor

    # bellman equation
    if not done:
        Q[prev_state[0], prev_state[1], prev_state[2], action] += alpha * \
            (reward + gamma * np.max(Q[next_state]) -
             Q[prev_state[0], prev_state[1], prev_state[2], action])
    else:
        Q[prev_state[0], prev_state[1], prev_state[2], action] += alpha * \
            (reward - Q[prev_state[0], prev_state[1], prev_state[2], action])


def showQ():
    for player_total in range(32):
        for dealer_card in range(12):
            for usable_ace in range(2):
                for action in range(2):
                    print("Q-value for state: ", player_total, ", ", dealer_card,
                          ", ", usable_ace, ": ", Q[player_total, dealer_card, usable_ace])
