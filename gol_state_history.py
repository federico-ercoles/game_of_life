import numpy as np
from random import random


class GameStateHistory:
    def __init__(self, state=np.zeros((10, 10), dtype=np.int16), max_history_length=15):
        self.index = 0
        self.history = [state]
        self.max_history_length = max_history_length

    def clear_history(self):
        del self.history[:]
        self.index = -1

    def current_state(self):
        return self.history[self.current_index()]

    def current_shape(self):
        return np.shape(self.current_state())

    def current_index(self):
        return self.index

    def add_state(self, state_matrix):
        if len(self.history) >= self.max_history_length:
            del self.history[0]
        else:
            self.index += 1
        self.history.append(state_matrix)

    def previous_state(self):
        if self.index >= 1:
            self.index -= 1

    def next_state(self):
        if self.current_index() + 1 < len(self.history):
            self.index += 1
        else:

            # life check; updates grid according to the following rules:
            # a live cell stays alive if it has exactly two or three live neighbors, dies otherwise;
            # a dead cell comes alive if it has exactly three live neighbors.

            def count_neighbours(state_matrix, x, y):
                # counts the amount of live cells around position (x, y)

                state_shape = np.shape(state_matrix)
                bordered_grid = np.zeros((state_shape[0] + 2, state_shape[1] + 2), dtype=np.int16)
                bordered_grid[1:state_shape[0] + 1, 1:state_shape[1] + 1] = state_matrix
                neighborhood = bordered_grid[x:x + 3, y:y + 3]
                neighborhood[1, 1] = 0
                return np.sum(neighborhood)

            shape = self.current_shape()
            new_state_matrix = np.zeros(shape, dtype=np.int16)
            for i in range(shape[0]):
                for j in range(shape[1]):
                    n = count_neighbours(self.current_state(), i, j)
                    if (self.current_state()[i][j] and (n in (2, 3))) or (not self.current_state()[i][j] and (n == 3)):
                        new_state_matrix[i][j] = 1
            self.add_state(new_state_matrix)

    def random_state(self):
        # returns a random configuration, with life probability 30%

        shape = self.current_shape()
        state_matrix = np.zeros(shape, dtype=np.int16)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if random() <= 0.3:
                    state_matrix[i, j] = 1
        self.clear_history()
        self.add_state(state_matrix)

    def empty_state(self, shape):
        self.clear_history()
        self.add_state(np.zeros(shape, dtype=np.int16))
