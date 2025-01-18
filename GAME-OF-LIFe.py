import pygame

# Initialize Pygame
pygame.init()

# Constants
grid_size = 80, 80  # Grid dimensions in tiles (rows, cols)
tile_size = 10       # Size of each tile in pixels
width, height = grid_size[1] * tile_size, grid_size[0] * tile_size + 50  # Screen dimensions

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 100, 200)

# Global variables
white = [[False for _ in range(grid_size[1])] for _ in range(grid_size[0])]  # List of tiles that are currently white
running = False
mouse_dragging = False
last_dragged = (-1, -1)

# Pygame setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tile Grid Toggle")
font = pygame.font.SysFont(None, 24)

def main():
    global running, mouse_dragging, last_dragged
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < grid_size[0] * tile_size:  # Grid area
                    toggle(x // tile_size, y // tile_size)
                    last_dragged = (x // tile_size, y // tile_size)
                    mouse_dragging = True
                elif width - 110 <= x <= width - 10 and grid_size[0] * tile_size <= y <= height:  # Button
                    running = not running
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_dragging = False
            elif event.type == pygame.MOUSEMOTION and mouse_dragging:
                x, y = event.pos
                if y < grid_size[0] * tile_size:  # Grid area
                    if (x // tile_size, y // tile_size) != last_dragged:
                        toggle(x // tile_size, y // tile_size)
                        last_dragged = (x // tile_size, y // tile_size)

        draw()
        logic()

        pygame.display.flip()
        clock.tick(60)

def draw():
    screen.fill(BLACK)
    draw_grid()
    draw_bottom_bar()

def draw_grid():
    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            color = WHITE if white[row][col] else BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def toggle(x, y):
    white[y][x] = not white[y][x]

def draw_bottom_bar():
    pygame.draw.rect(screen, GRAY, (0, grid_size[0] * tile_size, width, 50))
    count_text = font.render(f"White Tiles: {sum(sum(row) for row in white)}", True, BLACK)
    screen.blit(count_text, (10, grid_size[0] * tile_size + 15))

    button_color = (200, 200, 200) if running else WHITE
    button_rect = pygame.Rect(width - 110, grid_size[0] * tile_size + 10, 100, 30)
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    button_text = font.render("Stop" if running else "Start", True, BLACK)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

def logic():
    global white
    if running:
        new_white = [[False for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        for y in range(grid_size[0]):
            for x in range(grid_size[1]):
                surround = check(x, y)
                if white[y][x]:
                    if 2 <= surround <= 3:  # Survival
                        new_white[y][x] = True
                else:
                    if surround == 3:  # Reproduction
                        new_white[y][x] = True
        white = new_white

def check(x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                 (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
    return sum([white[ny][nx] for nx, ny in neighbors if 0 <= nx < grid_size[1] and 0 <= ny < grid_size[0]])

if __name__ == "__main__":
    main()
