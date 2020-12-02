from enviroment import Enviroment
from dqn.agent import Agent


class AiTraining():
    def __init__(self):
        self.actions = {1: self.train_agent, 2: self.play_game, 3: self.save_model, 4: self.load_model}
        self.enviroment = Enviroment()
        self.agent = Agent(gamma=0.99, epsilon=1, learning_rate=0.0001,
                           input_dims=self.enviroment.observation_space, output_dims=self.enviroment.action_space, 
                           memory_size=500000, eps_min=0.1, batch_size=512, replace=1000, eps_dec=2e-6, 
                           exploration_steps=20000)

    def start(self):
        print("Podaj akcję którą ma wykonać program:")
        print("(1) - Trenuj model")
        print("(2) - Zagraj w grę")
        print("(3) - Zapisz model")
        print("(4) - Wczytaj model")
        try:
            action = int(input())
        except ValueError:
            print("Wrong value.")
        while action != 0:
            if action in self.actions:
                self.actions[action]()
            print("Podaj akcję którą ma wykonać program:")
            print("(1) - Trenuj model")
            print("(2) - Zagraj w grę")
            print("(3) - Zapisz model")
            print("(4) - Wczytaj model")
            try:
                action = int(input())
            except ValueError:
                print("Wrong value.")

    def save_model(self):
        self.agent.save_model()

    def load_model(self):
        self.agent.load_model()

    def play_game(self):
        done = False
        observation = self.enviroment.reset(False)
        while not done:
            action = self.agent.choose_game_action(observation)
            observation_, reward, done = self.enviroment.step(action)
            observation = observation_
        self.enviroment.close()

    def train_agent(self):
        print("For how many games should the agent be played?")
        try:
            gamesToPlay = int(input())
        except ValueError:
            print("Wrong value.")
            return

        for i in range(gamesToPlay):
            done = False
            observation = self.enviroment.reset()

            score = 0
            steps = 0
            while not done:
                action = self.agent.choose_action(observation)
                observation_, reward, done = self.enviroment.step(action)
                score += reward
                self.agent.store_transition(observation, action, reward, observation_, done)
                self.agent.learn()
                observation = observation_
                steps += 1
                if steps > 10000:
                    print("Time limit exceeded")
                    break
            print("Gra nr." + str(i) + " Wynik: " + str(score) + " Epsilon: " + str(round(self.agent.epsilon, 3)) + " Steps: " + str(steps) )


aiTraining = AiTraining()
aiTraining.start()
