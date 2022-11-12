import random
import collections

Box = collections.namedtuple('Box', ('bottom', 'top', 'partition'))
PRESSURE_REDUCTION = 0.01


class Roulette:
    def __init__(self, values):
        self._boxes = []
        self._box_size = sum(values)
        self._stuff_into_boxes(values)

    def _stuff_into_boxes(self, values):
        pressure_reducer = PRESSURE_REDUCTION * max(values)
        values = [value + pressure_reducer for value in values]
        # Split values into matching boxes; if a box isn't full, add another value
        normal_values = [value * len(values) for value in values]
        large_values = {index: value for index, value in enumerate(normal_values) if value >= self._box_size}
        small_values = {index: value for index, value in enumerate(normal_values) if value < self._box_size}
        while len(small_values) > 0:
            top_value_index = next(iter(large_values))
            bottom_value_index, partition = small_values.popitem()
            self._boxes.append(Box(bottom_value_index, top_value_index, partition))
            large_values[top_value_index] -= self._box_size - partition
            if large_values[top_value_index] < self._box_size:
                small_values[top_value_index] = large_values.pop(top_value_index)
        self._boxes += [Box(0, value, 0) for value in large_values]

    def spin(self):
        box = random.choice(self._boxes)
        weight = random.randint(0, self._box_size)
        value_index = box.top if weight >= box.partition else box.bottom
        return value_index
