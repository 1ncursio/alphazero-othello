import numpy as np
import pickle


class Qplayer:
    def __init__(self, symbol, gama=0.9, sotf=0.7):
        self.symbol = symbol
        self.count = 0
        self.gama = gama
        self.soft = sotf
        self.states = []
        self.states_value = {}
        self.exp_rate = 0.15

    def update(self, postion):
        self.states.append(postion)

    def rewardUpdate(self, reward):
        for s in reversed(self.states):
            if self.states_value.get(s) is None:
                self.states_value[s] = 0
            self.states_value[s] += self.soft * \
                (self.gama * reward - self.states_value[s])
            reward = self.states_value[s]
        self.states = []

    def randomChoice(self, positions):
        idx = np.random.choice(len(positions))
        action = positions[idx]
        # print(action)
        return action

    def chooseAction(self, positions, current_board):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # print(np.random.uniform(0, 1),'zzz')
            return self.randomChoice(positions)
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = self.symbol
                next_boardHash = str(next_board.reshape(9))

                value = 0 if self.states_value.get(
                    next_boardHash) is None else self.states_value.get(next_boardHash)

                if value >= value_max:
                    value_max = value
                    action = p

            return action

    def save(self):
        with open('qValue.p', 'wb') as f:
            pickle.dump(self.states_value, f)
