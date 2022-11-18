from metugenetic.config import config


class Life:
    def __init__(self, size, initial_cells):
        self._size = size
        self.initial_cells = initial_cells
        self.cells = set(initial_cells)
        self._neighbour_positions = [-size - 1, -size, -size + 1, -1, 1, size - 1, size, size + 1]
        self._grid_size = size ** 2

    def simulate_until_repeat(self):
        configurations = [self.cells]
        for iteration in range(config.max_iterations):
            self.cycle()
            if self.cells in configurations:
                return iteration
            configurations.append(self.cells)
        print(f"WARNING: reached max iterations")
        return config.max_iterations

    def cycle(self):
        candidates = [self._candidate_position(cell, position)
                      for position in self._neighbour_positions
                      for cell in self.cells]
        self.cells = set(cell for cell in candidates if self._should_birth(candidates, cell))

    def _candidate_position(self, cell, position):
        if config.is_torus:
            return (cell + position) % self._grid_size
        return cell + position

    def _should_birth(self, candidates, cell):
        should_birth = 2 - (cell in self.cells) < candidates.count(cell) < 4
        within_bounds = 0 <= cell < self._grid_size
        return within_bounds and should_birth

    def print(self):
        for row in range(self._size):
            print(f"{row}: " + ''.join(' *' [row * self._size + column in self.cells] for column in range(self._size)))

