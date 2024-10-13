import pygame
from maze import generate_maze
from search import dfs

# Pygame initialization
pygame.init()

TILE_SIZE = 30
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# display
def setup_display(cols, rows):
    width = cols * TILE_SIZE
    height = rows * TILE_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Visualization")
    return screen

# arrow direction
def draw_arrow(screen, x, y, direction):
    center_x = x * TILE_SIZE + TILE_SIZE // 2
    center_y = y * TILE_SIZE + TILE_SIZE // 2
    size = TILE_SIZE // 3  # Arrow size

    if direction == "up":
        pygame.draw.polygon(screen, BLACK, [(center_x, center_y - size), (center_x - size // 2, center_y + size),
                                            (center_x + size // 2, center_y + size)])
    elif direction == "down":
        pygame.draw.polygon(screen, BLACK, [(center_x, center_y + size), (center_x - size // 2, center_y - size),
                                            (center_x + size // 2, center_y - size)])
    elif direction == "left":
        pygame.draw.polygon(screen, BLACK, [(center_x - size, center_y), (center_x + size, center_y - size // 2),
                                            (center_x + size, center_y + size // 2)])
    elif direction == "right":
        pygame.draw.polygon(screen, BLACK, [(center_x + size, center_y), (center_x - size, center_y - size // 2),
                                            (center_x - size, center_y + size // 2)])

# draw the maze
def draw_maze(screen, grid_cells, cols, rows, explored=None, path=None):
    screen.fill(WHITE)

    # draw path gray during DFS
    if explored:
        for cell in explored:
            x, y = cell
            pygame.draw.rect(screen, (200, 200, 200), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # draw correct path green
    if path:
        for (x, y) in path:
            pygame.draw.rect(screen, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw arrows
        for i in range(len(path) - 1):
            x, y = path[i]
            next_x, next_y = path[i + 1]
            if next_x > x:
                draw_arrow(screen, x, y, "right")
            elif next_x < x:
                draw_arrow(screen, x, y, "left")
            elif next_y > y:
                draw_arrow(screen, x, y, "down")
            elif next_y < y:
                draw_arrow(screen, x, y, "up")

    # draw walls
    for cell in grid_cells:
        x, y = cell.x * TILE_SIZE, cell.y * TILE_SIZE
        if cell.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + TILE_SIZE, y), 2)
        if cell.walls['right']:
            pygame.draw.line(screen, BLACK, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2)
        if cell.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), 2)
        if cell.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y + TILE_SIZE), (x, y), 2)

# visualisation of the maze/DFS
def main():
    # Ask user for maze dimensions before launching Pygame
    cols = int(input("Enter the number of columns for the maze: "))
    rows = int(input("Enter the number of rows for the maze: "))

    # display size
    screen = setup_display(cols, rows)

    # maze generator
    grid_cells = generate_maze(cols, rows)

    # var for DFS visualisation
    explored_cells = set()
    correct_path = []

    # start/goal
    start = (0, 0)
    goal = (cols - 1, rows - 1)  #

    clock = pygame.time.Clock()
    running = True
    solve_maze = False
    dfs_step = False

    # display maze
    draw_maze(screen, grid_cells, cols, rows)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve_maze = True
                    print("SPACE pressed...")

        if solve_maze and not dfs_step:
            print("DFS is starting...")
            # DFS call/run
            correct_path = dfs(grid_cells, start, goal, cols, explored_cells, screen, draw_maze, clock)
            dfs_step = True
            print("DFS completed.")

            # print correct path cells in terminal
            if correct_path:
                print(f"Correct path (total {len(correct_path)} cells):")
                # break every 10 cells
                for i in range(0, len(correct_path), 10):
                    chunk = correct_path[i:i + 10]
                    path_str = " -> ".join([f"({x}, {y})" for (x, y) in chunk])
                    print(path_str)
            else:
                print("No path found.")

        # draw correct/wrong paths
        draw_maze(screen, grid_cells, cols, rows, explored_cells, correct_path)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
