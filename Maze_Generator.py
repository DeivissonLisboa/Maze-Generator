import pygame, random
from datetime import datetime


# SCREEN SETUP
pygame.init()
WIDTH, HEIGHT = 600, 600
root = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE = "Maze Generator"
pygame.display.set_caption(TITLE)
FPS = 30

# GLOBALS
W = 20
COLS = ROWS = WIDTH // W

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VISITED_COLOR = (174, 197, 235)
CURRENT_COLOR = (237, 218, 109)


class Cell:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.color = BLACK
        self.statecolor = VISITED_COLOR
        self.x = x
        self.y = y
        self.posx = self.x * W
        self.posy = self.y * W
        self.stroke = 1
        self.walls = [True] * 4  # TOP, RIGHT, BOTTOM, LEFT
        self.rects = [
            (self.posx, self.posy, W, self.stroke),
            (self.posx + W - self.stroke, self.posy, self.stroke, W),
            (self.posx, self.posy + W - self.stroke, W, self.stroke),
            (self.posx, self.posy, self.stroke, W),
        ]
        self.state = False

    def draw(self):
        # if self.state:
        #     pygame.draw.rect(self.screen, self.statecolor, (self.posx, self.posy, W, W))
        for indexWall, wall in enumerate(self.walls):
            if wall:
                pygame.draw.rect(self.screen, self.color, self.rects[indexWall])

    def glow(self, color):
        pygame.draw.rect(self.screen, color, (self.posx, self.posy, W, W))

    def checkNeighbour(self, grid):
        neighbourhood = []

        if self.y >= 1:
            neighbourhood.append(grid[self.x][self.y - 1])
        if self.x < COLS - 1:
            neighbourhood.append(grid[self.x + 1][self.y])
        if self.y < COLS - 1:
            neighbourhood.append(grid[self.x][self.y + 1])
        if self.x >= 1:
            neighbourhood.append(grid[self.x - 1][self.y])

        arr = [i for i in neighbourhood if not i.state]
        if arr:
            return random.choice(arr)


def removeWalls(current, next):
    x = current.x - next.x
    if x == 1:
        current.walls[3] = False
        next.walls[1] = False
    elif x == -1:
        current.walls[1] = False
        next.walls[3] = False
    else:
        y = current.y - next.y
        if y == 1:
            current.walls[0] = False
            next.walls[2] = False
        elif y == -1:
            current.walls[2] = False
            next.walls[0] = False


# OBJECTS
grid = [[Cell(root, x, y) for y in range(COLS)] for x in range(ROWS)]
current = grid[0][0]
stack = []


def draw():
    global current
    global stack

    current.state = True
    next = current.checkNeighbour(grid)
    if next:
        next.state = True
        stack.append(current)
        removeWalls(current, next)
        current = next
    elif len(stack) > 0:
        current = stack.pop()

    root.fill(WHITE)
    for line in grid:
        for cell in line:
            cell.draw()
    current.glow(CURRENT_COLOR)

    pygame.display.update()


# MAIN LOOP
def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(root, f"{datetime.now()}.png")
                running = False
                pygame.quit()
        draw()


if __name__ == "__main__":
    main()
