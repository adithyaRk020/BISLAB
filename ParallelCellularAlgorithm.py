#Parallel Cell Algorithm
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Define the grid size
grid_size = 5  # Set a smaller grid for easier display, e.g., 10x10
grid = np.random.randint(0, 2, (grid_size, grid_size))

# Define a simple rule (e.g., Conway's Game of Life)
def game_of_life_cell(i, j, grid):
    # Count live neighbors
    neighbors = grid[i-1:i+2, j-1:j+2]
    total = np.sum(neighbors) - grid[i, j]
    if grid[i, j] == 1:
        return 1 if total in [2, 3] else 0
    else:
        return 1 if total == 3 else 0

def update_cell(i, j, grid):
    return game_of_life_cell(i, j, grid)

def parallel_update(grid):
    # Create a copy of the grid to store updated values
    new_grid = grid.copy()
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(1, grid.shape[0]-1):
            for j in range(1, grid.shape[1]-1):
                futures.append(executor.submit(update_cell, i, j, grid))
        # Collect results from the futures and update the new grid
        idx = 0
        for future in futures:
            i, j = divmod(idx, grid.shape[1] - 2)
            new_grid[i+1, j+1] = future.result()
            idx += 1
    return new_grid

# Update the grid
grid = parallel_update(grid)

# Display the grid as a matrix (instead of plotting)
print("Updated Grid after applying Conway's Game of Life rule:")
print(grid)

