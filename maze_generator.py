import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
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

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)

    def draw_current(self, screen):
        x = self.col * CELL_SIZE + CELL_SIZE // 4
        y = self.row * CELL_SIZE + CELL_SIZE // 4
        pygame.draw.rect(screen, RED, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

def create_grid():
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

        if generating:
            # Step 1: Get unvisited neighbors
            neighbors = get_unvisited_neighbors(current, grid)

            if neighbors:
                # Step 2: Choose random neighbor
                next_cell = random.choice(neighbors)

                # Step 3: Push current to stack
                stack.append(current)

                # Step 4: Remove wall between current and next
                remove_walls(current, next_cell)

                # Step 5: Mark next as visited and make it current
                next_cell.visited = True
                current = next_cell
            elif stack:
                current = stack.pop()
            else:
                generating = False

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
    generate_maze()
