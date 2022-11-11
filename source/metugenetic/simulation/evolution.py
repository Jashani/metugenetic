import metugenetic.simulation.life
import random
import pprint


class Evolution:
    def __init__(self, population_size, board_size):
        self._population = []
        self._generate_population(population_size, board_size)

    def run(self):
        evaluations = []
        for entity in self._population:
            evaluation = self._evaluate(entity)
            evaluations.append((evaluation, entity.initial_cells))
        evaluations.sort()
        pprint.pprint(evaluations)

    def _generate_population(self, population_size, board_size):
        maximum_cells = board_size ** 2
        sample = range(maximum_cells)
        for entity in range(population_size):
            cell_count = random.randint(0, maximum_cells - 1)
            cells = random.sample(sample, cell_count)
            life = metugenetic.simulation.life.Life(board_size, cells)
            self._population.append(life)

    def _evaluate(self, life):
        iterations = life.simulate_until_repeat()
        return iterations
