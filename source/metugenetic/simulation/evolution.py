import metugenetic.simulation.life
import metugenetic.simulation.roulette
import random

MUTATION_CHANCE = 0.1
FITTEST_COUNT = 1


class Evolution:
    def __init__(self, population_size, board_size):
        self._population = []
        self._board_size = board_size
        self._cell_count = board_size ** 2
        self._sample = range(self._cell_count)
        self._population_size = population_size

    def run(self, generations):
        self._generate_population()
        for generation in range(generations):
            evaluations = []
            for entity in self._population:
                evaluation = self._evaluate(entity)
                evaluations.append(evaluation)
            self._print_run_results(evaluations, generation)
            self._new_generation(evaluations)

    def _print_run_results(self, evaluations, generation):
        for_median = list(evaluations)  # Only for median
        for_median.sort()
        print(f"Generation {generation}:")
        print(f"\tHighest evaluation: {max(evaluations)}")
        print(f"\tLowest evaluation: {min(evaluations)}")
        print(f"\tAverage evaluation: {sum(evaluations) / len(evaluations)}")
        print(f"\tMedian evaluation: {for_median[int(len(for_median) / 2)]}")

    def _generate_population(self):
        self._population = []
        for entity in range(self._population_size):
            cells = self._random_cell_selection()
            life = metugenetic.simulation.life.Life(self._board_size, cells)
            self._population.append(life)

    def _random_cell_selection(self):
        cell_count = random.randint(0, self._cell_count - 1)
        cells = random.sample(self._sample, cell_count)
        return cells

    def _new_generation(self, evaluations):
        parents = self._pair_parents(evaluations, self._population_size - FITTEST_COUNT)
        the_fittest = self._the_fittest(evaluations)
        self._population = [metugenetic.simulation.life.Life(self._board_size, life.initial_cells) for life in the_fittest]
        for parent_1, parent_2 in parents:
            child = self._breed(parent_1, parent_2)
            self._population.append(child)

    def _the_fittest(self, evaluations):
        fittest = sorted(zip(evaluations, self._population), key=lambda pair: pair[0])[-FITTEST_COUNT:]
        individuals = [individual for evaluation, individual in fittest]
        print(f"Best config: {individuals[-1].initial_cells}")
        return individuals

    def _breed(self, parent_1, parent_2):
        # partition = random.randint(0, self._cell_count + 1)
        # parent_1_share = [cell for cell in parent_1.initial_cells if cell < partition]
        # parent_2_share = [cell for cell in parent_2.initial_cells if cell >= partition]
        # initial_cells = parent_1_share + parent_2_share

        initial_cells = []
        mask = self._random_cell_selection()
        for cell in range(self._cell_count):
            if cell in mask and cell in parent_1.initial_cells:
                initial_cells.append(cell)
            elif cell not in mask and cell in parent_2.initial_cells:
                initial_cells.append(cell)

        self._mutate(initial_cells)
        child = metugenetic.simulation.life.Life(self._board_size, initial_cells)
        return child

    def _mutate(self, cells):
        duplicates = len(self._population) - len(set(self._population))
        mutation_pusher = duplicates * 0.01
        for cell in range(self._cell_count):
            if not self._should_mutate(mutation_pusher):
                continue
            if cell in cells:
                cells.remove(cell)
            else:
                cells.append(cell)

    def _should_mutate(self, mutation_pusher):
        return random.random() < MUTATION_CHANCE + mutation_pusher

    def _evaluate(self, life):
        iterations = life.simulate_until_repeat()
        return iterations

    def _pair_parents(self, evaluations, children_needed):
        roulette = metugenetic.simulation.roulette.Roulette(evaluations)
        parent_pairs = []
        for _ in range(children_needed):
            parent_1_index, parent_2_index = self._select_parents(roulette)
            parent_pairs.append((self._population[parent_1_index], self._population[parent_2_index]))
        return parent_pairs

    def _select_parents(self, roulette):
        parent_1_index = roulette.spin()
        parent_2_index = roulette.spin()
        while parent_2_index == parent_1_index:
            parent_2_index = roulette.spin()
        return parent_1_index, parent_2_index