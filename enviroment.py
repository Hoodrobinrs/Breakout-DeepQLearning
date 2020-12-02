from breakout.main import Breakout

class Enviroment():
    """Enviroment for Deep Q Learning Example"""
    def __init__(self):
        self.__game = Breakout(True)
        self.__game.start()
        self.action_space = self.__game.get_output_size()
        self.observation_space = self.__game.get_input_size()
        self.ai = None

    def reset(self, ai=True):
        self.__game = Breakout(ai)
        self.__game.start()
        self.ai = ai
        return self.__game.get_observation()

    def step(self, action):
        return self.__game.step(action, not self.ai)

    def close(self):
        self.__game.close()