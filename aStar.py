import csv
import pygame
import time
import heapq
import glob

# Read grid from CSV
def read_grid_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [list(map(int, row)) for row in reader]

# Write grid to CSV
def write_grid_to_csv(file_path, grid):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(grid)

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algorithm with visualization
def a_star(grid, start, goal, screen, CELL_SIZE, MARGIN, quit_button_rect):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 4 possible movements

    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_score, node)
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    visited = set()

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        _, current = heapq.heappop(open_list)
        visited.add(current)

        # Visualize visited nodes
        if current != start and current != goal:
            grid[current[0]][current[1]] = 5  # Visited nodes (light blue)
            display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect)
            time.sleep(0.02)

        if current == goal:  # Path found
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Reverse the path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 0:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    came_from[neighbor] = current

                    if neighbor not in visited:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found

# Mark the path in the grid
def mark_path_in_grid(grid, path, screen, CELL_SIZE, MARGIN, quit_button_rect):
    for x, y in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        grid[x][y] = 4  # Mark path (deep blue)
        display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect)
        time.sleep(0.05)  # Delay for animation
    return grid

# Display the maze with Pygame
def display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect):
    BLACK = (0, 0, 0)  # Wall
    WHITE = (255, 255, 255)  # Path
    GREEN = (0, 255, 0)  # Start
    RED = (255, 0, 0)  # End
    LIGHT_BLUE = (173, 216, 230)  # Visited
    DEEP_BLUE = (0, 0, 255)  # Final Path
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
            elif grid[row][col] == 4:
                color = DEEP_BLUE
            elif grid[row][col] == 5:
                color = LIGHT_BLUE
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

    # Draw Quit button
    pygame.draw.rect(screen, (200, 0, 0), quit_button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("QUIT", True, WHITE)
    text_rect = text.get_rect(center=quit_button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

# Function to find the next available input file
def get_next_maze_input(directory):
    files = glob.glob(f"{directory}/maze_*.csv")
    if not files:
        return f"{directory}/maze_1.csv"
    indices = [int(f.split('_')[-1].split('.')[0]) for f in files]
    next_index = max(indices)
    return f"{directory}/maze_{next_index}.csv"

# Function to find the corresponding aStar output file name
def get_corresponding_aStar_file(input_directory, output_directory):
    maze_file = get_next_maze_input(input_directory)  # Get latest maze file
    maze_index = int(maze_file.split('_')[-1].split('.')[0])  # Extract the index
    return f"{output_directory}/aStar_{maze_index}.csv"


# Main function to execute A* and visualize the result
def main(input_directory, output_directory):
    input_file = get_next_maze_input(input_directory)
    grid = read_grid_from_csv(input_file)
    start = None
    goal = None

    # Find the start (2) and goal (3) positions in the grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 2:
                start = (r, c)
            if grid[r][c] == 3:
                goal = (r, c)

    if not start or not goal:
        print("Start or goal not found in the grid!")
        return

    pygame.init()
    CELL_SIZE = 20
    MARGIN = 2
    screen_width = (CELL_SIZE + MARGIN) * len(grid[0])
    screen_height = (CELL_SIZE + MARGIN) * len(grid) + 50  # Extra space for Quit button
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("A* Pathfinding Visualization")

    # Define Quit button
    quit_button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 40, 100, 30)

    # Run A* with visualization
    path = a_star(grid, start, goal, screen, CELL_SIZE, MARGIN, quit_button_rect)

    if path:
        # Mark the final path with animation
        mark_path_in_grid(grid, path, screen, CELL_SIZE, MARGIN, quit_button_rect)
        output_file = get_corresponding_aStar_file(input_directory, output_directory)
        write_grid_to_csv(output_file, grid)
        print(f"Path found and saved to {output_file}")
    else:
        print("No path found.")

    # Wait until the user closes the window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    running = False

    pygame.quit()

# Example usage
if __name__ == "__main__":
    input_directory = "AI_Maze_Solver\mazes_input"  # Path to input directory
    output_directory = "AI_Maze_Solver\mazes_output\aStar"  # Path to save output CSV file
    main(input_directory, output_directory)
