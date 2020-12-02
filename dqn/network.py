import torch

class Network(torch.nn.Module):
    """PyTorch AI Network"""
    def __init__(self, learning_rate: float, input_dims: int, output_dims: int):
        super(Network, self).__init__()

        self.fc1 = torch.nn.Linear(input_dims, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, output_dims)

        self.optimizer = torch.optim.RMSprop(self.parameters(), lr=learning_rate)

        self.loss = torch.nn.MSELoss()
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        state1 = torch.nn.functional.relu(self.fc1(state))
        state2 = torch.nn.functional.relu(self.fc2(state1))
        state3 = self.fc3(state2)
        return state3

    def save_checkpoint(self):
        pass

    def load_checkpoint(self):
        pass
