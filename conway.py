"""
Conway's Game of Life Rules:

    1. If a cell is ON and has fewer than two
    neighbors that are ON, it turns OFF.

    2. If a cell is ON and has either two or three
    neighbors that are ON, it remains ON.

    3. If a cell is ON and has more than three
    neighbors that are ON, it turns OFF.

    4. If a cell is OFF and has exactly three
    neighbors that are ON, it turns ON.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]


def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.6, 0.4]).reshape(N, N)


'''
Modulus Operator for Boundary Conditions:
(N*N grid)

>>> N = 16 
>>> i1 = 14 
>>> i2 = 15 
>>> (i1+1)%N 
15 
>>> (i2+1)%N 
0
'''


def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbours for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8 neighbour sum using toroidal bounds
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


def main():
    N = int(input("Enter the grid size: "))
    updateInterval = int(input("Enter the update interval (ms): "))
    grid = np.array([])
    grid = randomGrid(N)

    # set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), frames=10,
                                  interval=updateInterval, save_count=50)

    plt.show()


if __name__ == "__main__":
    main()
