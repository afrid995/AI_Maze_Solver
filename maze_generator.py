import pygame
import numpy as np
import random
import csv

# Function to check if a cell is inside the grid
def is_in_grid(pos, grid_dim):
    rows, cols = grid_dim
    x, y = pos
    return 0 <= x < rows and 0 <= y < cols

# Function to find valid neighbors for maze generation
def get_valid_neighbors(pos, grid, grid_dim):
    x, y = pos
    neighbors = []
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Moves in 2-cell steps
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_in_grid((nx, ny), grid_dim) and grid[nx, ny] == 0:
            neighbors.append(((nx, ny), (x + dx // 2, y + dy // 2)))  # Add path between cells
    
    return neighbors

# Function to generate the maze (animated)
def generate_maze(grid, start_pos, grid_dim, screen, CELL_SIZE, MARGIN, clock, quit_button_rect):
    stack = [start_pos]
    grid[start_pos] = 1  # Mark start as visited

    while stack:
        current = stack[-1]
        neighbors = get_valid_neighbors(current, grid, grid_dim)

        if neighbors:
            # Pick a random neighbor and carve the path
            (next_cell, path_cell) = random.choice(neighbors)
            grid[path_cell] = 1  # Carve the connecting cell
            grid[next_cell] = 1  # Mark the new cell as visited
            stack.append(next_cell)  # Add the new cell to the stack

            # Animate the maze generation
            display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect)
            clock.tick(30)  # Control animation speed
        else:
            stack.pop()  # Backtrack if no neighbors

    return grid

# Function to ensure multiple paths exist from start to end
def add_redundant_paths(grid, grid_dim, density=0.2):
    rows, cols = grid_dim
    for _ in range(int(rows * cols * density)):  # Add extra paths based on density
        x, y = random.randint(1, rows - 2), random.randint(1, cols - 2)
        if grid[x, y] == 0:  # Only carve new paths where there's a wall
            neighbors = get_valid_neighbors((x, y), grid, grid_dim)
            if neighbors:
                _, path_cell = random.choice(neighbors)
                grid[path_cell] = 1
                grid[x, y] = 1
    return grid

# Function to visualize the maze in pygame
def display_maze(grid, screen, CELL_SIZE, MARGIN, button_rects):
    BLACK = (0, 0, 0)  # Wall
    WHITE = (255, 255, 255)  # Path
    GREEN = (0, 255, 0)  # Start
    RED = (255, 0, 0)  # End
    rows, cols = len(grid), len(grid[0])

    screen.fill(WHITE)  # Clear screen

    for row in range(rows):
        for col in range(cols):
            color = BLACK
            if grid[row][col] == 1:
                color = WHITE
            elif grid[row][col] == 2:
                color = GREEN
            elif grid[row][col] == 3:
                color = RED
            pygame.draw.rect(
                screen,
                color,
                [
                    col * (CELL_SIZE + MARGIN),
                    row * (CELL_SIZE + MARGIN),
                    CELL_SIZE,
                    CELL_SIZE,
                ],
            )

    # Draw Quit and other buttons
    for rect, label in button_rects:
        pygame.draw.rect(screen, (200, 0, 0), rect)
        font = pygame.font.Font(None, 24)
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

def save_maze(grid, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)
    print(f"Maze saved to {file_path}")

# Function to find the next available maze index based on existing files
def get_next_maze_index(directory):
    i = 1
    while True:
        file_path = f"{directory}\\maze_{i}.csv"
        try:
            # Try to open the file to check if it exists
            with open(file_path, 'r'):
                # If file exists, increment and check the next index
                i += 1
        except FileNotFoundError:
            # If the file doesn't exist, return the current index
            return i

def main():
    pygame.init()
    CELL_SIZE, MARGIN, ROWS, COLS = 15, 2, 35, 35
    START_POS, END_POS = None, None
    screen_width, screen_height = COLS * (CELL_SIZE + MARGIN), ROWS * (CELL_SIZE + MARGIN) + 50
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Interactive Maze Generator")
    clock = pygame.time.Clock()

    button_width, button_height = 100, 40
    button_y = screen_height - 45
    button_rects = [
        (pygame.Rect(10, button_y, button_width, button_height), "Start Pos"),
        (pygame.Rect(160, button_y, button_width, button_height), "End Pos"),
        (pygame.Rect(310, button_y, button_width, button_height), "Generate"),
        (pygame.Rect(460, button_y, button_width, button_height), "Quit")
    ]
    
    grid = np.zeros((ROWS, COLS), dtype=int)
    setting_start, setting_end = False, False
    running = True

    # Get the next available maze index based on existing files
    maze_index = get_next_maze_index(r"C:\Users\prudhvi\OneDrive\Desktop\Afrid\maze project\maze final\mazes_input")
    
    # Define the file path to save the maze
    file_path = fr"C:\Users\prudhvi\OneDrive\Desktop\Afrid\maze project\maze final\mazes_input\maze_{maze_index}.csv"
    
    while running:
        display_maze(grid, screen, CELL_SIZE, MARGIN, button_rects)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, label in button_rects:
                    if rect.collidepoint(mouse_pos):
                        if label == "Quit":
                            running = False
                        elif label == "Start Pos":
                            setting_start = True
                            setting_end = False
                        elif label == "End Pos":
                            setting_start = False
                            setting_end = True
                        elif label == "Generate" and START_POS and END_POS:
                            # Generate the maze, add redundant paths and save it
                            grid = generate_maze(grid, START_POS, (ROWS, COLS), screen, CELL_SIZE, MARGIN, clock, button_rects)
                            grid = add_redundant_paths(grid, (ROWS, COLS), density=0.15)
                            grid[START_POS] = 2  # Mark start
                            grid[END_POS] = 3    # Mark end
                            save_maze(grid, file_path)
                            display_maze(grid, screen, CELL_SIZE, MARGIN, button_rects)
                
                col, row = mouse_pos[0] // (CELL_SIZE + MARGIN), mouse_pos[1] // (CELL_SIZE + MARGIN)
                if is_in_grid((row, col), (ROWS, COLS)):
                    if setting_start:
                        START_POS = (row, col)
                        grid[row, col] = 2  # Mark start position
                        setting_start = False
                    elif setting_end:
                        END_POS = (row, col)
                        grid[row, col] = 3  # Mark end position
                        setting_end = False
        
    pygame.quit()

if __name__ == "__main__":
    main()
