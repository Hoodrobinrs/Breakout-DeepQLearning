from enviroment import Enviroment
from dqn.agent import Agent

class AiTraining():
    def __init__(self):
        self.actions = {}
        self.enviroment = Enviroment()
        self.agent = Agent(gamma=0.99, epsilon=1, learning_rate=0.0001,
                           input_dims=self.enviroment.observation_space, output_dims=self.enviroment.action_space, 
                           memory_size=50000, eps_min=0.1, batch_size=32, replace=1000, eps_dec=0.1)

    def start(self):
        self.train_agent()

    def train_agent(self):
        print("For how many games should the agent be played?")
        try:
            gamesToPlay = int(input())
        except ValueError:
            print("Wrong value.")
            return

        for i in range(gamesToPlay):
            done = True
            observation = self.enviroment.reset()

            score = 0
            while done:
                action = self.agent.choose_action(observation)
                observation_, reward, done = self.enviroment.step(action)
                score += reward
                self.agent.store_transition(observation, action, reward, observation_, done)
                self.agent.learn()
            print("Gra nr." + str(i) + " Wynik: " + str(score))

    def play_game(self):
        pass

aiTraining = AiTraining()
aiTraining.start()
