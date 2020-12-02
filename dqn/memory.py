import numpy as np

class Memory(object):
    """Memory buffer of Agent used in Q Learning"""
    def __init__(self, memory_size: int, input_dims: int, output_dims: int):
        self.memory_size = memory_size
        self.memory_counter = 0

        print(input_dims)

        self.state_memory = np.zeros((self.memory_size, input_dims), dtype=np.float32)

        self.new_state_memory = np.zeros((self.memory_size, input_dims), dtype=np.float32)

        self.action_memory = np.zeros(self.memory_size, dtype=np.int64)
        self.reward_memory = np.zeros(self.memory_size, dtype=np.int64)
        self.terminal_memory = np.zeros(self.memory_size, dtype=np.bool)

    def store_transition(self, state, action, reward, state_, done):
        index = self.memory_counter % self.memory_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done
        self.memory_counter += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.memory_counter, self.memory_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        states_ = self.new_state_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal
