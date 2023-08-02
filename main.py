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

def readPattern(filename, grid):
    """This function reads in text files and updates the grid based on values that are in the text file.
       Text files should begin with the size of the numpy array / grid as the first line. All succeeding lines represent the values
       either 0 or 255 of the cell"""
    with open(fileName, 'r') as file:
        N = int(file.readline())            # The first line of the text file should be the size of the numpy array
        grid = np.zeros(N*N).reshape(N, N)  # Initialize the grid to just zeros
        for i in range(0, N - 1):
            for count, j in enumerate((file.readline()).split()):   # Split each line into a list of values either 0 or 255
                grid[i, count] = j
    return grid, N

def click(event):
    """This function captures the mouse position when it is clicked and changes the inhabiting cell's status"""
    newGrid = grid.copy()
    j = int(event.xdata)    # Capture cell by recording the x and y position of the mouse click
    i = int(event.ydata)
    if grid[i, j] == ON:
        newGrid[i, j] = OFF    # If the clicked cell is on then turn it off, if the clicked cell is off then turn it on
    else:
        newGrid[i, j] = ON
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    plt.show()              # Even if the game is paused, show the user which cells they have clicked
    return img

def pause(event):
    """This function captures key input and pauses the simulation if the space key has been pressed.
       The simulation resumes when the space key is pressed again."""
    global paused           # Access the paused boolean in the global scope
    key = event.key
    if key == " ":
        if paused:
            anim.resume()
            paused = False
        else:
            anim.pause()
            paused = True

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
    parser.add_argument('--readfile', dest='fileName', required=False)

    # Parse the command line arguments
    args = parser.parse_args()

    # Initialization
    N = 100
    if args.N and int(args.N) > 8 and int(args.N) <= 100:      # Set the grid size to 100 unless an argument greater than 8 and less than 100 was made
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
    if args.fileName:
        fileName = args.fileName
        grid, N = readPattern(fileName, grid)
    else:
        grid = randomGrid(N)                    # Create a grid full of random on and off cells
    
    fig, ax = plt.subplots()
    fig.set_facecolor("black")
    ax.spines['top'].set_color("white")
    ax.spines['bottom'].set_color("white")
    ax.spines['left'].set_color("white")
    ax.spines['right'].set_color("white")
    ax.text(N / 10, N / -15, "Conway's Game of Life", color='w', family='sans-serif', fontweight='bold', fontsize=16)
    img = ax.imshow(grid, interpolation='nearest', cmap='gray')

    anim = animation.FuncAnimation(fig, 
                                   update, 
                                   fargs=(img, grid, N, ),      # Update the animation every frame
                                   frames=10, 
                                   interval=updateInterval, 
                                   save_count=50)

    paused = False
    cidrelease = fig.canvas.mpl_connect('button_release_event', click)  # Set up the events for clicking and key presses
    cidkey = fig.canvas.mpl_connect('key_release_event', pause)

    if args.movfile:
        anim.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()