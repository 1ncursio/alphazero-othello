import numpy as np


class Border:
    def __init__(self, row=3, col=3, symbol=1):
        self.row = row
        self.col = col
        self.state = np.zeros((row, col))
        self.done = False
        self.symbol = symbol

    def reset(self):
        self.state = np.zeros((self.row, self.col))
        self.done = False
        self.symbol = 1

    def availablePositions(self):
        positions = []
        for i in range(self.row):
            for j in range(self.col):
                if self.state[i, j] == 0:
                    positions.append((i, j))
        return positions

    def getHash(self):
        return str(self.state.reshape(self.row * self.col))

    def soyobuCheck(self, endResult):
        for i in range(self.row):
            if sum(self.state[i, :]) == endResult:
                self.done = True

        for i in range(self.col):
            if sum(self.state[:, i]) == endResult:
                self.done = True
        diag_sum1 = sum([self.state[i, i] for i in range(3)])
        diag_sum2 = sum([self.state[i, 3 - i - 1]
                        for i in range(3)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if(diag_sum == 3):
            self.done = True

    def step(self, action, symbol):
        self.state[action] = symbol
        endResult = symbol*3

        self.soyobuCheck(endResult)

        if(self.done == False):
            self.symbol = self.symbol*-1

        return self.getHash()
