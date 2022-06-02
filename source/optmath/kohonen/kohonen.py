from typing import Callable, Optional, Tuple

import numpy as np
from numpy.typing import NDArray


def euclidean(
    first: NDArray[np.float64], second: NDArray[np.float64]
) -> NDArray[np.float64]:
    return np.sqrt(np.sum(np.square(first - second), axis=1))


class Kohonen:

    neurons: Optional[NDArray[np.float64]] = None
    n0: float = 1.0
    learning_rate: float = 1.0

    def __init__(
        self,
        shape: int,
        distance_function: Callable[
            [NDArray[np.float64], NDArray[np.float64]], NDArray[np.float64]
        ] = euclidean,
        learning_rate: float = 0.5,
        initializer: Callable[
            [Tuple[int, int, int]], NDArray[np.float64]
        ] = np.random.normal,
    ) -> None:
        self.shape = shape
        self.initializer = initializer
        self.distance_function = distance_function
        self.learning_rate = learning_rate

    def execute(self, x: NDArray[np.float64], epochs: int):  # n x t
        self.__current_train = x
        self.ensure_network()
        assert self.neurons is not None

        for sample in x:
            for t in range(epochs):
                vectorized_sample = np.full(
                    (self.shape, self.shape, self.depth), sample
                )
                distances = self.distance_function(
                    self.neurons, vectorized_sample
                )
                min_pos = np.unravel_index(
                    np.argmin(distances, axis=None), distances.shape
                )
                # update minimal neuron
                neuron = self.neurons[min_pos[0]][min_pos[1]]

                n = self.n0 * np.exp(-t * self.learning_rate)
                new_weight = neuron + n * (sample - neuron)

                self.neurons[min_pos[0]][min_pos[1]] = new_weight

        del self.__current_train

    def ensure_network(self):
        if self.neurons is None:
            assert len(self.__current_train.shape) == 2
            self.depth = self.__current_train.shape[1]
            self.neurons = self.initializer(
                size=(self.shape, self.shape, self.depth)
            )
