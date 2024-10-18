import unittest
import numpy as np
from grid import create_grid, place_obstacles
from agent import place_agent, place_survivors
from simulation import simulate
from agent import ObstacleType

class TestRescueSimulation(unittest.TestCase):

    def test_obstacle_placement(self):
        grid = create_grid(10, 10)
        place_obstacles(grid, 5)
        self.assertGreater(np.count_nonzero(grid), 0)  # Check that obstacles were placed

    def test_survivor_placement(self):
        grid = create_grid(10, 10)
        place_survivors(grid, 3)
        self.assertEqual(np.count_nonzero(grid == -1), 3)  # Check that 3 survivors were placed

    def test_pathfinding_with_obstacles(self):
        grid = create_grid(10, 10)
        place_obstacles(grid, 2) #Place 2 obstacles
        place_survivors(grid,1) #Place 1 survivor
        place_agent(grid)
        survivors_before = np.count_nonzero(grid==-1)
        simulate(grid,(0,0))
        survivors_after = np.count_nonzero(grid==-1)
        self.assertLess(survivors_after, survivors_before) #Check that at least one survivor was rescued


    def test_no_path(self):
        grid = create_grid(10,10)
        place_obstacles(grid, 50) #Place many obstacles
        place_survivors(grid,1) #Place 1 survivor
        place_agent(grid)
        survivors_before = np.count_nonzero(grid==-1)
        simulate(grid,(0,0))
        survivors_after = np.count_nonzero(grid==-1)
        self.assertEqual(survivors_after, survivors_before) #Check that no survivors were rescued


if __name__ == '__main__':
    unittest.main()
