from dqn.memory import Memory
from dqn.network import Network

import numpy as np
import torch

class Agent():
    """Deep Q Learning Agent"""
    def __init__(self, gamma: float, epsilon: float, learning_rate: float,
                 input_dims: tuple, output_dims: tuple, memory_size: int, batch_size: int,
                 eps_min: float = 0.01, eps_dec: float = 4e-7, replace: int = 1000, exploration_steps: int = 100):
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.input_tims = input_dims
        self.output_dims = output_dims
        self.output_space = [i for i in range(output_dims)]
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.replace = replace
        self.exploration_steps = exploration_steps

        self.step_counter = 0
        self.not_learning_step_counter = 0

        self.memory = Memory(memory_size, input_dims, output_dims)

        self.q_network = Network(learning_rate, input_dims, output_dims)

        self.q_network_next = Network(learning_rate, input_dims, output_dims)

    def choose_action(self, observation):
        if np.random.random() > self.epsilon and self.exploration_steps < self.not_learning_step_counter:
            state = torch.tensor([observation], dtype=torch.float).to(self.q_network.device)
            actions = self.q_network.forward(state)
            action = torch.argmax(actions).item()
        else:
            action = np.random.choice(self.output_space)
        return action

    def choose_game_action(self, observation):
        state = torch.tensor([observation], dtype=torch.float).to(self.q_network.device)
        actions = self.q_network.forward(state)
        print(actions)
        action = torch.argmax(actions).item()
        return action

    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def sample_memory(self):
        state, action, reward, new_state, done = \
        self.memory.sample_buffer(self.batch_size)

        states = torch.tensor(state).to(self.q_network.device)
        rewards = torch.tensor(reward).to(self.q_network.device)
        dones = torch.tensor(done).to(self.q_network.device)
        actions = torch.tensor(action).to(self.q_network.device)
        states_ = torch.tensor(new_state).to(self.q_network.device)

        return states, actions, rewards, states_, dones

    def replace_target_network(self):
        if self.step_counter & self.replace == 0:
            self.q_network_next.load_state_dict(self.q_network.state_dict())

    def decrement_epsilon(self):
        self.epsilon = self.epsilon - self.eps_dec \
                           if self.epsilon > self.eps_min else self.eps_min
        
    def learn(self):
        self.not_learning_step_counter += 1
        if self.memory.memory_counter < self.batch_size:
            return
        self.q_network.optimizer.zero_grad()

        self.replace_target_network()

        states, actions, rewards, states_, dones = self.sample_memory()
        indices = np.arange(self.batch_size)

        q_pred = self.q_network.forward(states)[indices, actions]
        q_next = self.q_network_next.forward(states_).max(dim=1)[0]

        q_next[dones] = 0.0
        q_target = rewards + self.gamma*q_next

        loss = self.q_network.loss(q_target, q_pred).to(self.q_network.device)
        loss.backward()
        self.q_network.optimizer.step()
        self.step_counter += 1

        if self.exploration_steps < self.not_learning_step_counter:
            self.decrement_epsilon()

    def save_model(self):
        torch.save(self.q_network.state_dict(), "qNetwork.model")
        torch.save(self.q_network_next.state_dict(), "qNetworkNext.model")

    def load_model(self):
        self.q_network.load_state_dict(torch.load("qNetwork.model"))
        self.q_network_next.load_state_dict(torch.load("qNetworkNext.model"))