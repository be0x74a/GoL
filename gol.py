import pyglet
import numpy as np

WIDTH=1366
HEIGHT=720
SQUARE_SIZE=10
RATIO=0.5
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
            rgb_int = squares[square] % 0xFFFFFF
            color = (rgb_int & 255, (rgb_int >> 8) & 255, (rgb_int >> 16) & 255)
            color = (128, 128, 128)
            batch_squares.append(pyglet.shapes.Rectangle(square[0]*SQUARE_SIZE, square[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, color=color, batch=batch))
        batch.draw()

def life_happens():

    birth_cells = []
    dead_cells = []
    potential_birth_cells = {}

    for coord in squares.keys():
        neighbors_count = get_neighbors_count(*coord, potential_birth_cells)[0]
        if neighbors_count >= 4:
            dead_cells.append(coord)
        if neighbors_count <= 1:
            dead_cells.append(coord)

    for coord in potential_birth_cells.keys():
        count, gen = get_neighbors_count(*coord, {})
        if count == 3:
            birth_cells.append(coord)

    for coord in dead_cells:
        squares.pop(coord)

    for coord in birth_cells:
        squares[coord] = 1

def get_neighbors_count(x, y, potential_birth_cells):
    c = 0
    gen = 0

    neighbors_coords = [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y), (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]

    for coord in neighbors_coords:
        c, gen = evaluate_neighbour(*coord, c, gen, potential_birth_cells)

    return c, gen + 1

def evaluate_neighbour(x, y, c, gen, potential_birth_cells):
    if 0 <= x * SQUARE_SIZE < WIDTH and 0 <= y * SQUARE_SIZE <= HEIGHT and (x, y) in squares:
        return c+1, max(gen, squares[(x,y)])
    else:
        potential_birth_cells[(x,y)] = 1
        return c, gen

if __name__ == '__main__':
    initial_squares = tuple(zip(*np.where(np.random.choice(2, (WIDTH//SQUARE_SIZE, HEIGHT//SQUARE_SIZE), p=[1-RATIO, RATIO]) == 1)))
    for square in initial_squares:
        squares[(square[0], square[1])] = 1

    window = Window()
    pyglet.app.run()