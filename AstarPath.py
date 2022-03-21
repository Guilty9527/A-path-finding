import pygame
from queue import PriorityQueue

EDGE = 400  # size of window
WIN = pygame.display.set_mode((EDGE, EDGE))  # Window
pygame.display.set_caption("MAZE SOLVING!")  # Title

# Colour settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)


class Node:
    def __init__(self, row, col, edge, total_rows):  # initialize the variables
        self.row = row
        self.col = col
        self.x = row * edge
        self.y = col * edge
        self.color = BLACK
        self.neighbors = []
        self.edge = edge
        self.total_rows = total_rows

    def get_pos(self):  # initialize the variables
        return self.row, self.col

    def is_closed(self):  # condition by colour
        return self.color == GREEN

    def is_open(self):  # condition by colour
        return self.color == RED

    def is_barrier(self):  # condition by colour
        return self.color == WHITE

    def is_start(self):  # condition by colour
        return self.color == ORANGE

    def is_end(self):  # condition by colour
        return self.color == ORANGE

    def reset(self):  # set colour for the action
        self.color = BLACK

    def make_start(self):  # set colour for the action
        self.color = ORANGE

    def make_closed(self):  # set colour for the action
        self.color = GREEN

    def make_open(self):  # set colour for the action
        self.color = RED

    def make_barrier(self):  # set colour for the action
        self.color = WHITE

    def make_end(self):  # set colour for the action
        self.color = ORANGE

    def make_path(self):  # set colour for the action
        self.color = PURPLE

    def draw(self, win):  # draw the window and the grid with size 1
        pygame.draw.rect(win, self.color, (self.x, self.y, self.edge, self.edge))

    def update_neighbors(self, grid):  # make a list and if there is no stop in the direction add grid to the list
        self.neighbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def h(p1, p2):  # the formula for the estimate distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:  # while current is in the list
        current = came_from[current]  # from the end to the start
        current.make_path()  # make it a path
        draw()  # draw it


def algorithm(draw, grid, start, end):
    count = 0  # count tracking
    open_set = PriorityQueue()  # make a priority queue
    open_set.put((0, count, start))  # add nodes  to the queue
    came_from = {}  # track what node did the node come from
    g_score = {node: float("inf") for row in grid for node in row}  # store the g in formula short path from start
    g_score[start] = 0  # set g node as start to 0
    f_score = {node: float("inf") for row in grid for node in row}  # store the h estimate short path to end node
    f_score[start] = h(start.get_pos(), end.get_pos())  # update the pos

    open_set_hash = {start}  # keep track all the item in the priority queue

    while not open_set.empty():  # if every single empty set has been checked quit the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  # if reached the end node we reconstruct it
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # take the distance and add 1 for the neighbor

            if temp_g_score < g_score[neighbor]:  # if detected a shorter path
                came_from[neighbor] = current  # came from the neighbor of the current
                g_score[neighbor] = temp_g_score  # replace the g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())  # update the F
                if neighbor not in open_set_hash:  # dont get the repeat grid
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))  # add it to open_set
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # make it open
        draw()

        if current != start:  # if it is no start node
            current.make_closed()  # make it close

    return False


def make_grid(rows, edge):  # set how many rows and divided the whole screen to grid
    grid = []
    gap = edge // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, edge):  # draw grid from 0 to size of edge in each gap on row and colum
    gap = edge // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (edge, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, edge))


def draw(win, grid, rows, edge):  # fill the grid with black
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, edge)
    pygame.display.update()


def get_clicked_pos(pos, rows, edge):  # set each cube in the grid as a position
    gap = edge // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, edge):  # main
    nog = 40  # number of grids
    grid = make_grid(nog, edge)  # make grid

    start = None
    end = None
    running = True

    while running:  # keep looping the main program
        draw(win, grid, nog, edge)  # firstly draw the window and grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # if quit end the loop
                running = False

            if pygame.mouse.get_pressed()[0]:  # if press left mouse button
                pos = pygame.mouse.get_pos()  # get position based on grid
                row, col = get_clicked_pos(pos, nog, edge)
                node = grid[row][col]
                if not start and node != end:  # if there is no start node and the position not end node make start node
                    start = node
                    start.make_start()

                elif not end and node != start:  # if there is no end node and the position not start node make end node
                    end = node
                    end.make_end()

                elif node != end and node != start:  # then if not on the position of start and end node make it barrier
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # else if right mouse button pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, nog, edge)
                node = grid[row][col]  # the node you click
                node.reset()  # reset it to nothing
                if node == start:  # if you click start node then cancel start node
                    start = None
                elif node == end:  # if you click end node then cancel end node
                    end = None

            elif event.type == pygame.KEYDOWN:  # if keyboard has been pressed
                if event.key == pygame.K_SPACE and start and end:  # if press space and there is both start and end node
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)  # call neighbour in the grid

                    algorithm(lambda: draw(win, grid, nog, edge), grid, start, end)  # then call A* algorithm

                if event.key == pygame.K_c:  # if press c
                    start = None
                    end = None
                    grid = make_grid(nog, edge)  # clear start and end node and make panel back to empty

    pygame.quit()


main(WIN, EDGE)  # call main
