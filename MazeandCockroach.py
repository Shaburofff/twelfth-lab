import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

SIZE = 11

def make_maze(width, height):
    maze = [[1] * width for _ in range(height)] 

    def carve(x, y):
        maze[y][x] = 0  
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                maze[y + dy//2][x + dx//2] = 0 
                carve(nx, ny)

    carve(1, 1) 
    return maze

def dfs_with_animation(maze, start, exit_pos, display, img, pause=0.1):
    visited = set()
    path = []
    found_path = []

    def dfs(x, y):
        if (x, y) == exit_pos:
            found_path.extend(path + [(x, y)])
            return True
        if x < 0 or x >= len(maze[0]) or y < 0 or y >= len(maze):
            return False
        if (x, y) in visited or maze[y][x] == 1:
            return False

        visited.add((x, y))
        path.append((x, y))

        if (x, y) != start and (x, y) != exit_pos:
            display[y][x] = 5
        img.set_data(display)
        plt.pause(pause)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if dfs(x + dx, y + dy):
                return True

        path.pop()
        if (x, y) != start and (x, y) != exit_pos:
            display[y][x] = 4 
        img.set_data(display)
        plt.pause(pause * 0.7)
        return False

    dfs(start[0], start[1])
    return found_path

def main():
    maze = make_maze(SIZE, SIZE)
    start = (1, 1)
    exit_pos = (SIZE - 2, SIZE - 2)
    maze[start[1]][start[0]] = 'S'
    maze[exit_pos[1]][exit_pos[0]] = 'E'

    display = [[0] * SIZE for _ in range(SIZE)]
    for y in range(SIZE):
        for x in range(SIZE):
            if maze[y][x] == 1:
                display[y][x] = 1
            elif maze[y][x] == 'S':
                display[y][x] = 2
            elif maze[y][x] == 'E':
                display[y][x] = 3
            else:
                display[y][x] = 0

    cmap = mcolors.ListedColormap(['white', 'black', 'green', 'red', 'lightgray', 'orange'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    img = ax.imshow(display, cmap=cmap, norm=norm, origin='upper')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Таракан ищет путь")
    plt.show()

    final_path = dfs_with_animation(maze, start, exit_pos, display, img, pause=0.15)

    if final_path:
        for x, y in final_path[1:-1]:
            display[y][x] = 5
        plt.title("Выход найден)")
    else:
        plt.title("Выход не найден(")

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
