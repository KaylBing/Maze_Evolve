import pygame
import random
import time

# Initialize pygame
pygame.init()

# Configurable parameters
MAZE_SIZE = "large"  # Options: "small", "medium", "large", "huge"

# Size presets
size_presets = {
    "small": {"cell": 40, "width": 800, "height": 800},
    "medium": {"cell": 30, "width": 900, "height": 900},
    "large": {"cell": 20, "width": 1000, "height": 1000},
    "huge": {"cell": 15, "width": 1200, "height": 1200}
}

# Set constants based on preset
CELL_SIZE = size_presets[MAZE_SIZE]["cell"]
WIDTH = size_presets[MAZE_SIZE]["width"]
HEIGHT = size_presets[MAZE_SIZE]["height"]
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Maze Generator ({MAZE_SIZE} - {COLS}x{ROWS})")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def get_pos(self):
        return self.row, self.col

    def draw(self, screen):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        wall_thickness = 1 if CELL_SIZE < 20 else 2  # Thinner walls for small cells

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), wall_thickness)
        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), wall_thickness)
        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), wall_thickness)
        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), wall_thickness)

    def draw_current(self, screen):
        x = self.col * CELL_SIZE + CELL_SIZE // 4
        y = self.row * CELL_SIZE + CELL_SIZE // 4
        pygame.draw.rect(screen, RED, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

def create_grid():
    print(f"Creating grid: {COLS}x{ROWS} (Total cells: {COLS*ROWS})")
    grid = []
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            grid[row].append(Cell(row, col))
    return grid

def remove_walls(current, next):
    dx = current.col - next.col
    dy = current.row - next.row

    if dx == 1:  # next is to the left
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:  # next is to the right
        current.walls['right'] = False
        next.walls['left'] = False

    if dy == 1:  # next is above
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:  # next is below
        current.walls['bottom'] = False
        next.walls['top'] = False

def get_unvisited_neighbors(cell, grid):
    neighbors = []
    row, col = cell.get_pos()

    if row > 0 and not grid[row-1][col].visited:  # top
        neighbors.append(grid[row-1][col])
    if col < COLS - 1 and not grid[row][col+1].visited:  # right
        neighbors.append(grid[row][col+1])
    if row < ROWS - 1 and not grid[row+1][col].visited:  # bottom
        neighbors.append(grid[row+1][col])
    if col > 0 and not grid[row][col-1].visited:  # left
        neighbors.append(grid[row][col-1])

    return neighbors

def generate_maze():
    grid = create_grid()
    stack = []
    current = grid[0][0]
    current.visited = True

    running = True
    generating = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not generating:
                    generating = True
                    grid = create_grid()
                    stack = []
                    current = grid[0][0]
                    current.visited = True
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if generating:
            neighbors = get_unvisited_neighbors(current, grid)

            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(current)
                remove_walls(current, next_cell)
                next_cell.visited = True
                current = next_cell
            elif stack:
                current = stack.pop()
            else:
                generating = False
                print("Maze generation complete!")

        # Draw everything
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw(screen)

        if generating:
            current.draw_current(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    print(f"Generating {MAZE_SIZE} maze ({COLS}x{ROWS})")
    generate_maze()
