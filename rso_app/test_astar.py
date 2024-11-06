import unittest
import numpy as np
from astar import astar

class TestAStar(unittest.TestCase):

    def test_astar_simple(self):
        grid = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        start = (0, 0)
        end = (2, 2)
        path = astar(grid, start, end, allow_diagonal=False)
        self.assertIsNotNone(path)

    def test_astar_obstacle(self):
        grid = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        start = (0, 0)
        end = (2, 2)
        path = astar(grid, start, end, allow_diagonal=False)
        self.assertIsNotNone(path)

    def test_astar_obstacle_diagonal(self):
        grid = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        start = (0, 0)
        end = (2, 2)
        path = astar(grid, start, end, allow_diagonal=True)
        self.assertIsNotNone(path)

    def test_astar_no_path(self):
        grid = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ])
        start = (0, 0)
        end = (2, 2)
        path = astar(grid, start, end, allow_diagonal=False)
        self.assertIsNone(path)

    def test_astar_no_path_diagonal(self):
        grid = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ])
        start = (0, 0)
        end = (2, 2)
        path = astar(grid, start, end, allow_diagonal=True)
        self.assertIsNone(path)


if __name__ == '__main__':
    unittest.main()
