import pyglet
import numpy as np

WIDTH=1366
HEIGHT=720
SQUARE_SIZE=10
np.random.seed(42)

squares = {}

class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__(WIDTH, HEIGHT, vsync = False)
        pyglet.clock.schedule_interval(self.update, 1.0/60)

    def update(self, dt): 
        pass

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        batch = pyglet.graphics.Batch()
        batch_squares = []

        life_happens()

        for square in squares.keys():
            batch_squares.append(pyglet.shapes.Rectangle(square[0]*SQUARE_SIZE, square[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, color=(61, 255, 197), batch=batch))
        batch.draw()

def life_happens():

    dead_cells = []
    birth_cells = []
    potential_birth_cells = {}

    for coord in squares.keys():
        neighbors_count = get_neighbors_count(*coord, potential_birth_cells)
        if neighbors_count >= 4:
            dead_cells.append(coord)
        if neighbors_count <= 1:
            dead_cells.append(coord)
    
    for coord in potential_birth_cells.keys():
        if get_neighbors_count(*coord, {}) == 3:
            birth_cells.append(coord)

    for coord in dead_cells:
        squares.pop(coord)
    for coord in birth_cells:
        squares[coord] = 1

def get_neighbors_count(x, y, potential_birth_cells):
    c = 0
    if (x-1, y-1) in squares:
        c += 1
    else:
        potential_birth_cells[(x-1, y-1)] = 1
    if (x, y-1) in squares:
        c += 1
    else:
        potential_birth_cells[(x, y-1)] = 1
    if (x+1, y-1) in squares:
        c += 1
    else:
        potential_birth_cells[(x+1, y-1)] = 1
    if (x-1, y) in squares:
        c += 1
    else:
        potential_birth_cells[(x-1, y)] = 1
    if (x+1, y) in squares:
        c += 1
    else:
        potential_birth_cells[(x+1, y)] = 1
    if (x-1, y+1) in squares:
        c += 1
    else:
        potential_birth_cells[(x-1, y+1)] = 1
    if (x, y+1) in squares:
        c += 1
    else:
        potential_birth_cells[(x, y+1)] = 1
    if (x+1, y+1) in squares:
        c += 1
    else:
        potential_birth_cells[(x+1, y+1)] = 1
    return c

if __name__ == '__main__':
    initial_squares = tuple(zip(*np.where(np.random.randint(2, size=(WIDTH//SQUARE_SIZE, HEIGHT//SQUARE_SIZE)) == 1)))
    for square in initial_squares:
        squares[(square[0], square[1])] = 1

    window = Window()
    pyglet.app.run()