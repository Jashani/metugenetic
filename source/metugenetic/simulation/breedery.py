import bisect
import random
import metugenetic.simulation.life
import metugenetic.simulation.roulette
from metugenetic.config import config


class Breedery:
    def __init__(self, population_size, board_size):
        self.population = []
        self._board_size = board_size
        self._cell_count = board_size ** 2
        self._sample = range(self._cell_count)
        self.population_size = population_size
        self._fittest_maximum = int(population_size / config.fittest_limiter)

        config.crossover_methods = {'mask': self._mask_crossover,
                             'partition': self._partition_crossover}
        self._crossover = config.crossover_methods[config.crossover_method]

    def generate_population(self):
        self.population = []
        for _ in range(self.population_size):
            cells = self._random_cell_selection()
            life = metugenetic.simulation.life.Life(self._board_size, cells)
            self.population.append(life)

    def new_generation(self, evaluations):
        the_fittest = self._the_fittest(evaluations)
        parents = self._pair_parents(evaluations, self.population_size - len(the_fittest))
        self.population = [metugenetic.simulation.life.Life(self._board_size, life.initial_cells) for life in the_fittest]
        for parent_1, parent_2 in parents:
            child = self._breed(parent_1, parent_2)
            self.population.append(child)

    def _random_cell_selection(self):
        cell_count = random.randint(0, self._cell_count - 1)
        cells = random.sample(self._sample, cell_count)
        return cells

    def _the_fittest(self, evaluations):
        fittest_count = random.randint(config.fittest_minimum, self._fittest_maximum)
        fittest = sorted(zip(evaluations, self.population), key=lambda pair: pair[0])[-fittest_count:]
        individuals = [individual for evaluation, individual in fittest]
        print(f"Best config: {individuals[-1].initial_cells}")
        return individuals

    def _breed(self, parent_1, parent_2):
        initial_cells = self._crossover(parent_1, parent_2)
        self._mutate(initial_cells)
        child = metugenetic.simulation.life.Life(self._board_size, initial_cells)
        return child

    def _partition_crossover(self, parent_1, parent_2):
        partition = random.randint(0, self._cell_count + 1)
        parent_1_share = [cell for cell in parent_1.initial_cells if cell < partition]
        parent_2_share = [cell for cell in parent_2.initial_cells if cell >= partition]
        initial_cells = parent_1_share + parent_2_share
        return initial_cells

    def _mask_crossover(self, parent_1, parent_2):
        initial_cells = []
        mask = self._random_cell_selection()
        for cell in range(self._cell_count):
            if cell in mask and cell in parent_1.initial_cells:
                initial_cells.append(cell)
            elif cell not in mask and cell in parent_2.initial_cells:
                initial_cells.append(cell)
        return initial_cells

    def _mutate(self, cells):
        existing_configurations = set([tuple(life.initial_cells) for life in self.population])
        duplicates = len(self.population) - len(existing_configurations)
        mutation_pusher = duplicates * config.twin_avoidance_factor
        for cell in range(self._cell_count):
            if not self._should_mutate(mutation_pusher):
                continue
            if cell in cells:
                cells.remove(cell)
            else:
                bisect.insort(cells, cell)

    def _should_mutate(self, mutation_pusher):
        return random.random() < config.mutation_chance + mutation_pusher

    def _pair_parents(self, evaluations, children_needed):
        roulette = metugenetic.simulation.roulette.Roulette(evaluations)
        parent_pairs = []
        for _ in range(children_needed):
            parent_1_index, parent_2_index = self._select_parents(roulette)
            parent_pairs.append((self.population[parent_1_index], self.population[parent_2_index]))
        return parent_pairs

    def _select_parents(self, roulette):
        parent_1_index = roulette.spin()
        parent_2_index = roulette.spin()
        while parent_2_index == parent_1_index:
            parent_2_index = roulette.spin()
        return parent_1_index, parent_2_index