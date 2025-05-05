import pygame
import sys
from maze_generator import *  # Assuming your maze generator is in maze_generator.py

class MazeSolver:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.path = []
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.solution_found = False
        self.current_cell = None

    def get_neighbors(self, row, col):
        neighbors = []
        current = self.grid[row][col]

        # Check each direction if there's no wall
        if not current.walls['top'] and row > 0:
            neighbors.append((row-1, col))
        if not current.walls['right'] and col < self.cols-1:
            neighbors.append((row, col+1))
        if not current.walls['bottom'] and row < self.rows-1:
            neighbors.append((row+1, col))
        if not current.walls['left'] and col > 0:
            neighbors.append((row, col-1))

        return neighbors

    def solve(self, row=0, col=0):
        # Mark current cell as visited
        self.visited[row][col] = True
        self.current_cell = (row, col)

        # If we've reached the end
        if row == self.rows-1 and col == self.cols-1:
            self.solution_found = True
            self.path.append((row, col))
            return True

        # Get all accessible neighbors
        neighbors = self.get_neighbors(row, col)

        for neighbor_row, neighbor_col in neighbors:
            if not self.visited[neighbor_row][neighbor_col]:
                if self.solve(neighbor_row, neighbor_col):
                    self.path.append((row, col))
                    return True

        return False

    def draw_solution(self, screen):
        if not self.solution_found:
            return

        # Draw the solution path
        for row, col in self.path:
            x = col * CELL_SIZE + CELL_SIZE // 4
            y = row * CELL_SIZE + CELL_SIZE // 4
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

        # Draw current cell being explored
        if self.current_cell:
            row, col = self.current_cell
            x = col * CELL_SIZE + CELL_SIZE // 4
            y = row * CELL_SIZE + CELL_SIZE // 4
            pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

def main():
    # Generate a maze first
    grid = create_grid()
    generate_maze_instant(grid)  # We'll modify this to generate instantly

    # Initialize solver
    solver = MazeSolver(grid)

    # Set up pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()

    solving = False
    solved = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving and not solved:
                    solving = True
                    # Start solving in a new thread or we'll freeze the display
                    solver.solve()
                    solved = True
                    solving = False
                elif event.key == pygame.K_r:  # Reset
                    grid = create_grid()
                    generate_maze_instant(grid)
                    solver = MazeSolver(grid)
                    solved = False

        # Draw everything
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw(screen)

        if solved:
            solver.draw_solution(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def generate_maze_instant(grid):
    """Modified version of maze generation that completes instantly"""
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
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
            break

if __name__ == "__main__":
    main()
