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
        [0, 0, 255],
        [255, 0, 255],
        [0, 255, 255]
    ])
    grid[i:i + 3, j:j + 3] = glider

def update(frameNum, img, grid, N):
    pass

if __name__ == "__main__":
    """This program is designed to simulate John Conway's Game of Life"""

    # Create command line argument parser
    parser = argparse.ArgumentParser(description="Run simulation of Conway's Game of Life")

    # Create command line arguments
    parser.add_argument('--gridsize', dest='N', required=False)
    parser.add_argument('--movfile', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)

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