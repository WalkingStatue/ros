# Rescue Operation Simulator (ROS)

## Overview

The Rescue Operation Simulator (ROS) is a Python-based project that simulates autonomous agents navigating a disaster-stricken area to rescue survivors. It uses the A* search algorithm for path planning, considering obstacles, terrain costs, and agent capabilities.  ROS provides a flexible platform for experimenting with different algorithms, agent behaviors, and environmental conditions.

## Features

- **Grid-Based Environment:** Customizable grid for flexible scenario creation. Define grid size, place obstacles (buildings, ruins), and position survivors.
- **Autonomous Agents:** Agents navigate autonomously to rescue survivors.
- **Dynamic Pathfinding:** Uses the A* algorithm with options for diagonal movement and terrain cost assignment (roads, forests, rubble).
- **Obstacle Avoidance:** Agents avoid obstacles and dynamically replan paths.
- **Visualization:** Visual feedback of the grid, agents, survivors, and obstacles.

## Project Structure

The project is organized as follows:

- `rso_app/`: Contains the core simulation logic.
    - `agent.py`: Agent class and behavior.
    - `astar.py`: A* search algorithm implementation.
    - `grid.py`: Grid representation and management.
    - `grid_utils.py`: Utility functions for grid operations.
    - `main.py`: Main script to run the simulation.
    - `simulation.py`: Simulation logic and control.
    - `test_astar.py`: Unit tests for the A* algorithm.
    - `visualize.py`: Visualization functions.
- `rso_app/images/`: Contains images used in the visualization.

## Installation

1. **Clone the Repository:** `git clone https://github.com/WalkingStatue/rso.git`
2. **Install Dependencies:** `pip install -r requirements.txt`

## Usage

1. **Run the Simulation:** `python rso_app/main.py`
2. **Configure Parameters (Optional):** Modify parameters in `rso_app/main.py` (grid size, survivors, obstacles).