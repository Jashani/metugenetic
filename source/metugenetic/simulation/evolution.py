import metugenetic.simulation.breedery
import metugenetic.simulation.presentation

class Evolution:
    def __init__(self, population_size, board_size):
        self._breedery = metugenetic.simulation.breedery.Breedery(population_size, board_size)

    def run(self, generations):
        presentation = metugenetic.simulation.presentation.Presentation()
        self._breedery.generate_population()
        for generation in range(generations):
            evaluations = []
            for entity in self._breedery.population:
                evaluation = self._evaluate(entity)
                evaluations.append(evaluation)
            presentation.append(evaluations)
            self._breedery.new_generation(evaluations)
        presentation.graph()

    def _evaluate(self, life):
        iterations = life.simulate_until_repeat()
        return iterations
