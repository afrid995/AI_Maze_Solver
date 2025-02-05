import csv
import pygame
import time
import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def read_grid_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [list(map(int, row)) for row in reader]

def write_grid_to_csv(file_path, grid):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(grid)

def write_grid_to_pdf(file_path, grid):
    """Generate a PDF representation of the solved maze."""
    cell_size = 10
    margin = 5
    width = len(grid[0]) * cell_size + 2 * margin
    height = len(grid) * cell_size + 2 * margin

    c = canvas.Canvas(file_path, pagesize=(width, height))
    
    colors = {
        0: (0, 0, 0),  # Wall (Black)
        1: (255, 255, 255),  # Path (White)
        2: (0, 255, 0),  # Start (Green)
        3: (255, 0, 0),  # Goal (Red)
        4: (0, 0, 255),  # Final Path (Deep Blue)
        5: (173, 216, 230)  # Explored Path (Light Blue)
    }

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = colors.get(grid[row][col], (0, 0, 0))
            c.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)
            c.rect(margin + col * cell_size, height - (margin + (row + 1) * cell_size), cell_size, cell_size, fill=1)

    c.save()

def get_corresponding_dfs_files(input_directory, csv_output_directory, pdf_output_directory):
    maze_file = get_next_maze_input(input_directory)
    maze_index = int(maze_file.split('_')[-1].split('.')[0])  # Extract the index
    csv_path = f"{csv_output_directory}/bfs_{maze_index}.csv"
    pdf_path = f"{pdf_output_directory}/bfs_{maze_index}.pdf"
    return csv_path, pdf_path

def get_next_maze_input(directory):
    files = glob.glob(f"{directory}/maze_*.csv")
    if not files:
        return f"{directory}/maze_1.csv"
    indices = [int(f.split('_')[-1].split('.')[0]) for f in files]
    next_index = max(indices)
    return f"{directory}/maze_{next_index}.csv"

def bfs(grid, start, goal, screen, CELL_SIZE, MARGIN, quit_button_rect):
    from collections import deque
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([start])
    visited = set()
    came_from = {start: None}
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        current = queue.popleft()
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        if current not in visited:
            visited.add(current)
            grid[current[0]][current[1]] = 5
            display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect)
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 0:
                    if neighbor not in visited:
                        came_from[neighbor] = current
                        queue.append(neighbor)
    
    return None

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
        
        grid[x][y] = 4
        display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect)
    return grid

def display_maze(grid, screen, CELL_SIZE, MARGIN, quit_button_rect):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_BLUE = (173, 216, 230)
    DEEP_BLUE = (0, 0, 255)
    rows, cols = len(grid), len(grid[0])
    screen.fill(WHITE)
    
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
    pygame.draw.rect(screen, (200, 0, 0), quit_button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("QUIT", True, WHITE)
    text_rect = text.get_rect(center=quit_button_rect.center)
    screen.blit(text, text_rect)
    pygame.display.flip()

def main(input_directory, csv_output_directory, pdf_output_directory):
    input_file = get_next_maze_input(input_directory)
    grid = read_grid_from_csv(input_file)
    start, goal = None, None
    
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
    CELL_SIZE, MARGIN = 15, 2
    screen_width = (CELL_SIZE + MARGIN) * len(grid[0])
    screen_height = (CELL_SIZE + MARGIN) * len(grid) + 50
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BFS Pathfinding Visualization")
    quit_button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 40, 100, 30)
    
    path = bfs(grid, start, goal, screen, CELL_SIZE, MARGIN, quit_button_rect) 
    
    if path:
        mark_path_in_grid(grid, path, screen, CELL_SIZE, MARGIN, quit_button_rect)
        csv_file, pdf_file = get_corresponding_dfs_files(input_directory, csv_output_directory, pdf_output_directory)
        write_grid_to_csv(csv_file, grid)
        write_grid_to_pdf(pdf_file, grid)
        print(f"Path saved to:\nCSV: {csv_file}\nPDF: {pdf_file}")
    else:
        print("No path found.")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and quit_button_rect.collidepoint(event.pos):
                running = False
    pygame.quit()

if __name__ == "__main__":
    input_directory = r"AI_Maze_Solver\mazes_input"
    csv_output_directory = r"AI_Maze_Solver\mazes_output_csv\bfs"
    pdf_output_directory = r"AI_Maze_Solver\mazes_output_pdf\bfs"
    main(input_directory, csv_output_directory, pdf_output_directory)
