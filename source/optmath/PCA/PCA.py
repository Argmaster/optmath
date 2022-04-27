from dataclasses import dataclass, field
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from .. import RecordBase, to_numpy_array


@dataclass
class PCA:

    autoscaled_data: Tuple[RecordBase]
    np_data: NDArray[np.float64] = field(init=False)
    correlation_matrix: NDArray[np.float64] = field(init=False)
    sorted_eigenval_vector_pairs: Tuple[float, NDArray[np.float64]] = field(
        init=False
    )

    def __post_init__(self):
        self.np_data = to_numpy_array(self.autoscaled_data)
        self.correlation_matrix = (self.np_data.T @ self.np_data) / (
            self.np_data.shape[0]
        )

    def execute(self):
        eigenvalue = np.linalg.eig(self.correlation_matrix)
        self.sorted_eigenval_vector_pairs = sorted(
            zip(*eigenvalue), key=lambda e: e[0], reverse=True
        )

    @property
    def lambdas(self):
        return [l for l, _ in self.sorted_eigenval_vector_pairs]

    def scree_plot(self):
        x = np.arange(1, len(self.all_eigenvalue_vector_pairs()) + 1)
        plt.plot(x, self.lambdas)
        plt.scatter(x, self.lambdas)
        plt.title(
            f"Scree Plot for PCA on {len(self.autoscaled_data)} {self.autoscaled_data[0].class_name()} objects"
        )
        plt.ylabel("λ (eigenvalue)")
        plt.xlabel("Principal components")
        plt.xticks(x, [f"PC{i}" for i in x])
        plt.grid(True)

    def percent_scree_plot(self):
        x = np.arange(1, len(self.all_eigenvalue_vector_pairs()) + 1)
        m = len(self.autoscaled_data[0].numeric())
        prct_lambdas = [v / m for v in self.lambdas]
        label = "% of variance explained"
        plt.plot(x, prct_lambdas)
        plt.scatter(x, prct_lambdas)
        plt.title(
            f"Scree Plot for PCA on {len(self.autoscaled_data)} {self.autoscaled_data[0].class_name()} objects"
        )
        plt.ylabel(label)
        y = np.linspace(
            min(prct_lambdas), max(prct_lambdas), len(prct_lambdas)
        )
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xlabel("Principal components")
        plt.xticks(x, [f"PC{i}" for i in x])
        plt.grid(True)

    def cumulative_percent_scree_plot(self):
        x = np.arange(0, len(self.all_eigenvalue_vector_pairs()) + 1)
        m = len(self.autoscaled_data[0].numeric())
        prct_lambdas = [0.0]
        total = 0
        for v in self.lambdas:
            total += v / m
            prct_lambdas.append(total)
        label = "Cumulative % of variance explained"

        plt.plot(x, prct_lambdas)
        plt.scatter(x, prct_lambdas)
        plt.title(
            f"Scree Plot for PCA on {len(self.autoscaled_data)} {self.autoscaled_data[0].class_name()} objects"
        )
        plt.ylabel(label)
        y = np.linspace(
            min(prct_lambdas), max(prct_lambdas), len(prct_lambdas)
        )
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xlabel("Principal components")
        plt.xticks(x, [""] + [f"PC{i}" for i in x[1:]])
        plt.grid(True)

    def all_eigenvalue_vector_pairs(self):
        return self.sorted_eigenval_vector_pairs

    def from_kaiser_criteria(self, treshold: float = 0.95):
        return filter(
            lambda o: o[0] > treshold, self.all_eigenvalue_vector_pairs()
        )
