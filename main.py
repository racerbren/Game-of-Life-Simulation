import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """Creates a random grid of size N by N"""
    return np.random.choice(vals, N*N, p=[0.3, 0.7]).reshape(N, N)

def addGlider(i, j, grid):
    """Adds a common pattern which seemingly glides in one direction"""
    glider = np.array([
        [OFF, OFF, ON],
        [ON, OFF, ON],
        [OFF, ON, ON]
    ])
    grid[i:i + 3, j:j + 3] = glider

def addGosperGun(i, j, grid):
    """Adds a gosper glider gun pattern to the grid"""
    gosper = np.array([
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON],
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON],
        [ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
        [ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, ON, OFF, ON, ON, OFF, OFF, OFF, OFF, ON, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF], 
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF, OFF, OFF, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON, ON, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]
    ])
    grid[i:i + 9, j:j + 36] = gosper

def update(frameNum, img, grid, N):
    """This function updates the grid every frame"""
    newGrid = grid.copy()
    # For every cell in the grid, check all 8 of its surrounding neighbors
    for i in range(N):
        for j in range(N):
            # Modulus operators allow for checking cells that are at the edge
            # If a cell we are checking is past the edge, or has value of N, then reset to 0
            # If a cell we are checking has negative value, then reset to N - 1
            # This allows the simulation to operate infinitely on a 2D grid
            total = int((grid[i, (j - 1) % N] +             # Check the left neighbor
                         grid[i, (j + 1) % N] +             # Check the right neighbor
                         grid[(i - 1) % N, j] +             # Check the top neighbor
                         grid[(i + 1) % N, j] +             # Check the bottom neighbor
                         grid[(i - 1) % N, (j - 1) % N] +   # Check the top left neighbor
                         grid[(i - 1) % N, (j + 1) % N] +   # Check the top right neighbor
                         grid[(i + 1) % N, (j - 1) % N] +   # Check the bottom left neighbor
                         grid[(i + 1) % N, (j + 1) % N]     # Check the bottom right neighbor
                        ) / 255)                            # Divide by 255 to get a single digit number, 0-8
            
            # If the current cell is ON, check the rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            # If the current cell is OFF, check the rules
            else:
                if total == 3:
                    newGrid[i, j] = ON

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

if __name__ == "__main__":
    """This program is designed to simulate John Conway's Game of Life"""

    # Create command line argument parser
    parser = argparse.ArgumentParser(description="Run simulation of Conway's Game of Life")

    # Create command line arguments
    parser.add_argument('--gridsize', dest='N', required=False)
    parser.add_argument('--movfile', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)

    # Parse the command line arguments
    args = parser.parse_args()

    # Initialization
    N = 100
    if args.N and int(args.N) > 8:      # Set the grid size to 100 unless an argument greater than 8 was made
        N = int(args.N)
    
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)     # Set the anmation update interval
    
    # Create the grid
    grid = np.array([])
    if args.glider:
        grid = np.zeros(N*N).reshape(N,N)       # Create a grid full of off cells and add a glider pattern to the top left
        addGlider(1, 1, grid)
    if args.gosper:
        grid = np.zeros(N*N).reshape(N, N)      # Create a grid full of off cells and add the gosper gun pattern t the top left
        addGosperGun(1, 1, grid)
    else:
        grid = randomGrid(N)                    # Create a grid full of random on and off cells
    
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, 
                                   update, 
                                   fargs=(img, grid, N, ), 
                                   frames=10, 
                                   interval=updateInterval, 
                                   save_count=50)
    if args.movfile:
        anim.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()