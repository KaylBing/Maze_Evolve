import os
import shutil
import time
from terrible_solver import TerribleSolver, generate_maze_instant, create_grid, WIDTH, HEIGHT, CELL_SIZE

def create_test_directory(base_path, run_number):
    """Creates a numbered directory for this test run"""
    path = os.path.join(base_path, f"run_{run_number:03d}")
    os.makedirs(path, exist_ok=True)
    return path

def save_solver_code(directory):
    """Saves a copy of the solver code to the directory"""
    source_file = "terrible_solver.py"
    dest_file = os.path.join(directory, "solver_code.py")
    shutil.copyfile(source_file, dest_file)

def run_single_test(run_number, output_base):
    """Runs one test of the maze solver"""
    # Create test directory
    test_dir = create_test_directory(output_base, run_number)

    # Generate maze
    grid = create_grid()
    generate_maze_instant(grid)

    # Initialize solver
    solver = TerribleSolver(grid)

    # Run solver
    start_time = time.time()
    while not solver.solved and not solver.gave_up:
        solver.make_move()
    end_time = time.time()

    # Save results
    result = {
        'run_number': run_number,
        'steps': solver.steps,
        'solved': solver.solved,
        'time_seconds': end_time - start_time,
        'maze_size': f"{len(grid)}x{len(grid[0])}",
        'cell_size': CELL_SIZE,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Write results to file
    with open(os.path.join(test_dir, "results.txt"), 'w') as f:
        for key, value in result.items():
            f.write(f"{key}: {value}\n")

    # Save solver code
    save_solver_code(test_dir)

    return result

def run_batch_tests(output_base="maze_solver_runs", num_runs=100):
    """Runs multiple tests of the maze solver"""
    # Create output base directory
    os.makedirs(output_base, exist_ok=True)

    # Run all tests
    summary = []
    for run in range(1, num_runs + 1):
        print(f"Starting run {run}/{num_runs}...")
        result = run_single_test(run, output_base)
        summary.append(result)
        status = "SOLVED" if result['solved'] else "GAVE UP"
        print(f"Run {run} complete: {status} in {result['steps']} steps")

    # Save summary file
    with open(os.path.join(output_base, "summary.txt"), 'w') as f:
        f.write("Maze Solver Batch Test Summary\n")
        f.write("="*40 + "\n\n")
        f.write(f"Total runs: {num_runs}\n")
        f.write(f"Successful solves: {sum(1 for r in summary if r['solved'])}\n")
        f.write(f"Failures: {sum(1 for r in summary if not r['solved'])}\n\n")

        f.write("Run Details:\n")
        f.write("-"*40 + "\n")
        for run in summary:
            f.write(f"Run {run['run_number']:3d}: ")
            f.write(f"{'Solved' if run['solved'] else 'Failed':7} ")
            f.write(f"in {run['steps']:5d} steps, ")
            f.write(f"{run['time_seconds']:.2f} sec\n")

if __name__ == "__main__":
    print("Starting maze solver batch test...")
    run_batch_tests()
    print("All tests completed. Results saved in 'maze_solver_runs' directory.")
