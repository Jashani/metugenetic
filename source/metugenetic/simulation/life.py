
MAX_ITERATIONS = 1000


class Life:
    def __init__(self, size, initial_cells):
        self._size = size
        self.initial_cells = initial_cells
        self.cells = initial_cells
        self._neighbour_positions = [-size - 1, -size, -size + 1, -1, 1, size - 1, size, size + 1]
        self._grid_size = size ** 2

    def simulate_until_repeat(self):
        configurations = [self.cells]
        for iteration in range(MAX_ITERATIONS):
            self.cycle()
            if self.cells in configurations:
                return iteration
            configurations.append(self.cells)

    def cycle(self):
        candidates = [(cell + position) % self._grid_size
                      for position in self._neighbour_positions
                      for cell in self.cells]
        self.cells = set(cell for cell in candidates if self._should_birth(candidates, cell))

    def _should_birth(self, candidates, cell):
        return 2 - (cell in self.cells) < candidates.count(cell) < 4

    def print(self):
        for row in range(self._size):
            print(f"{row}: " + ''.join(' *' [row * self._size + column in self.cells] for column in range(self._size)))

