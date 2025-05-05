import pygame
import random
import time
from maze_generator import *

class TerribleSolver:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.path = []
        self.current_pos = (0, 0)  # Start at top-left
        self.end_pos = (self.rows-1, self.cols-1)  # End at bottom-right
        self.visited = set()
        self.steps = 0
        self.max_steps = 1000000  # Give up after this many steps
        self.solved = False
        self.gave_up = False

    def get_possible_moves(self, row, col):
        """Returns all possible moves from current position (ignores walls because this solver is terrible)"""
        moves = []
        if row > 0:
            moves.append((row-1, col))  # Up
        if row < self.rows-1:
            moves.append((row+1, col))  # Down
        if col > 0:
            moves.append((row, col-1))  # Left
        if col < self.cols-1:
            moves.append((row, col+1))  # Right
        return moves

    def make_move(self):
        """Makes one terrible move"""
        if self.solved or self.gave_up:
            return

        self.steps += 1
        if self.steps > self.max_steps:
            self.gave_up = True
            return

        row, col = self.current_pos
        self.visited.add((row, col))

        # Check if we've reached the end by pure luck
        if (row, col) == self.end_pos:
            self.solved = True
            return

        # Get all possible moves (ignoring walls because we're terrible)
        possible_moves = self.get_possible_moves(row, col)

        # Choose a completely random move (even if it's through a wall!)
        new_row, new_col = random.choice(possible_moves)

        # Actually check if we can move there (but only after choosing)
        current_cell = self.grid[row][col]
        new_cell = self.grid[new_row][new_col]

        # Determine direction
        if new_row < row:  # Moving up
            can_move = not current_cell.walls['top'] and not new_cell.walls['bottom']
        elif new_row > row:  # Moving down
            can_move = not current_cell.walls['bottom'] and not new_cell.walls['top']
        elif new_col < col:  # Moving left
            can_move = not current_cell.walls['left'] and not new_cell.walls['right']
        else:  # Moving right
            can_move = not current_cell.walls['right'] and not new_cell.walls['left']

        if can_move:
            self.current_pos = (new_row, new_col)
            self.path.append((new_row, new_col))
        else:
            # 50% chance to teleport to a random visited cell because why not
            if random.random() < 0.5 and len(self.visited) > 0:
                self.current_pos = random.choice(list(self.visited))

    def draw_state(self, screen):
        # Draw visited cells
        for row, col in self.visited:
            x = col * CELL_SIZE + CELL_SIZE // 4
            y = row * CELL_SIZE + CELL_SIZE // 4
            pygame.draw.rect(screen, (200, 200, 200), (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

        # Draw current path
        for row, col in self.path:
            x = col * CELL_SIZE + CELL_SIZE // 4
            y = row * CELL_SIZE + CELL_SIZE // 4
            pygame.draw.rect(screen, (255, 165, 0), (x, y, CELL_SIZE // 2, CELL_SIZE // 2))  # Orange

        # Draw current position
        row, col = self.current_pos
        x = col * CELL_SIZE + CELL_SIZE // 4
        y = row * CELL_SIZE + CELL_SIZE // 4
        pygame.draw.rect(screen, RED, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

        # Draw end position
        row, col = self.end_pos
        x = col * CELL_SIZE + CELL_SIZE // 4
        y = row * CELL_SIZE + CELL_SIZE // 4
        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE // 2, CELL_SIZE // 2))

        # Display status
        font = pygame.font.SysFont(None, 24)
        status = "Solved!" if self.solved else "Gave up :(" if self.gave_up else f"Steps: {self.steps}"
        text = font.render(status, True, BLACK)
        screen.blit(text, (10, 10))

def main():
    # Generate a maze first
    grid = create_grid()
    generate_maze_instant(grid)

    # Initialize terrible solver
    solver = TerribleSolver(grid)

    # Set up pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Terrible Maze Solver")
    clock = pygame.time.Clock()

    running = True
    solving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving:
                    solving = True
                elif event.key == pygame.K_r:  # Reset
                    grid = create_grid()
                    generate_maze_instant(grid)
                    solver = TerribleSolver(grid)
                    solving = False

        if solving and not solver.solved and not solver.gave_up:
            solver.make_move()
            time.sleep(0.01)  # Slow down so we can watch the terrible decisions

        # Draw everything
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                cell.draw(screen)

        solver.draw_state(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

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
