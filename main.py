import pygame
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

def main():
    pygame.init()
    
    # Screen dimensions
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Solver")
    
    # Button properties
    button_width, button_height = 150, 50
    button_y = 100
    button_spacing = 20
    buttons = [
        (pygame.Rect(225, button_y, button_width, button_height), "Generate", "maze_generator.py"),
        (pygame.Rect(225, button_y + button_height + button_spacing, button_width, button_height), "DFS", "dfs.py"),
        (pygame.Rect(225, button_y + 2 * (button_height + button_spacing), button_width, button_height), "A*", "aStar.py"),
        (pygame.Rect(225, button_y + 3 * (button_height + button_spacing), button_width, button_height), "BFS", "bfs.py"),
        (pygame.Rect(225, button_y + 4 * (button_height + button_spacing), button_width, button_height), "Quit", None)
    ]
    
    running = True
    while running:
        screen.fill((255, 255, 255))  # Clear screen
        
        # Draw buttons
        for rect, label, _ in buttons:
            pygame.draw.rect(screen, (0, 0, 200), rect)
            font = pygame.font.Font(None, 36)
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, _, script in buttons:
                    if rect.collidepoint(mouse_pos):
                        if script:
                            run_script(script)
                        else:
                            running = False
                            
    pygame.quit()

if __name__ == "__main__":
    main()
