# The Brainy Bunch: Intelligent Maze Navigation

This project simulates an intelligent agent navigating a maze. The agent explores the maze, avoiding walls, poison, and trying to find health items and the exit portal. It learns from its environment and can backtrack or retry based on its previous experience.

## Features

- **Random Maze Generation**: The maze is generated based on a predefined map, with random placements of the agent, portal, poison, and health items.
- **Agent Intelligence**: The agent explores the maze by making random movements, avoiding traps, and collecting health if necessary.
- **Backtracking**: The agent can backtrack if it encounters dead ends or dangerous situations.
- **Graphical Representation**: The maze and agent's actions are displayed using **Pygame**.

## Prerequisites

Before running the project, ensure you have:

- **Python 3.x** installed.
- **Pygame** library installed. The shell script provided will handle this for you if it's missing.

## Running the Program

### Using the Shell Script

1. **Clone the repository** or download the files to your local machine.

2. **Run the shell script** to build and run the program:

   ```bash
   ./run_program.sh



Here’s a README file in raw markdown for your project:

README.md
markdown
Copy code
# The Brainy Bunch: Intelligent Maze Navigation

This project simulates an intelligent agent navigating a maze. The agent explores the maze, avoiding walls, poison, and trying to find health items and the exit portal. It learns from its environment and can backtrack or retry based on its previous experience.

## Features

- **Random Maze Generation**: The maze is generated based on a predefined map, with random placements of the agent, portal, poison, and health items.
- **Agent Intelligence**: The agent explores the maze by making random movements, avoiding traps, and collecting health if necessary.
- **Backtracking**: The agent can backtrack if it encounters dead ends or dangerous situations.
- **Graphical Representation**: The maze and agent's actions are displayed using **Pygame**.

## Prerequisites

Before running the project, ensure you have:

- **Python 3.x** installed.
- **Pygame** library installed. The shell script provided will handle this for you if it's missing.

## Running the Program

### Using the Shell Script

1. **Clone the repository** or download the files to your local machine.

2. **Run the shell script** to build and run the program:

   ```bash
   ./run_program.sh



### How the Program Works
   The maze is a grid-based system where:
   
   Walls are represented as green blocks.
   The Agent (Voldemort) is represented as a red block.
   Portal (goal) is represented as a purple block.
   Poison is represented as black blocks.
   Health items are represented as yellow blocks.
   The agent makes random decisions on movement, avoids traps, and searches for the portal.
   
   If the agent encounters health, its health points increase.
   
   If the agent encounters poison, it loses health points.
   
   The game ends if the agent's health reaches zero or if the agent finds the portal.

   The program will start, and you'll see the maze and agent's exploration on the window.
Manual Execution
If you prefer to run the program manually:

#### Install dependencies:

```bash
pip3 install pygame
```
#### Run the Python program:

```bash
python3 main.py
```

