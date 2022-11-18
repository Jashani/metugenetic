import matplotlib.pyplot as plt
import numpy
import box


class Presentation:
    def __init__(self):
        self._data = box.Box(highest=[], lowest=[], average=[], median=[])

    def append(self, evaluations):
        print(f"EVALUATIONS: {evaluations}")
        self._data.highest.append(max(evaluations))
        self._data.lowest.append(min(evaluations))
        self._data.average.append(sum(evaluations) / len(evaluations))
        for_median = list(evaluations)  # Only for median
        for_median.sort()
        self._data.median.append(for_median[int(len(for_median) / 2)])
        self._print_latest_results()

    def graph(self):
        cycles = [cycle + 1 for cycle in range(len(self._data.highest))]
        figure, (values, standard) = plt.subplots(2, sharex=True, figsize=(10, 8))
        self._plot_data(self._data, cycles, values)
        standardised_data = self._standardised_data()
        self._plot_data(standardised_data, cycles, standard)
        plt.xlabel('Generation')
        values.set_ylabel('Value')
        standard.set_ylabel('Standardised Value')
        plt.suptitle(f'Evaluations')
        print("Graphing")
        plt.legend()
        plt.show()

    def _plot_data(self, data, cycles, values):
        values.axhline(y=0, color='black')
        values.plot(cycles, data.highest, label='Highest')
        values.plot(cycles, data.lowest, label='Lowest')
        values.plot(cycles, data.average, label='Average')
        values.plot(cycles, data.median, label='Median')

    def _standardised_data(self):
        standardised_data = box.Box(highest=[], lowest=[], average=[], median=[])
        standardised_data.highest = self._standardise(self._data.highest)
        standardised_data.lowest = self._standardise(self._data.lowest)
        standardised_data.average = self._standardise(self._data.average)
        standardised_data.median = self._standardise(self._data.median)
        return standardised_data

    def _standardise(self, data):
        average = numpy.average(data)
        standard_deviation = numpy.std(data)
        standardised = [(point - average) / standard_deviation for point in data]
        return standardised

    def _print_latest_results(self):
        print(f"Generation {len(self._data.highest)}:")
        print(f"\tHighest evaluation: {self._data.highest[-1]}")
        print(f"\tLowest evaluation: {self._data.lowest[-1]}")
        print(f"\tAverage evaluation: {self._data.average[-1]}")
        print(f"\tMedian evaluation: {self._data.median[-1]}")
