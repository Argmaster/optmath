from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .. import RecordBase, to_numpy_array


def PCA(autoscaled_data: Tuple[RecordBase]):
    nd_data = to_numpy_array(autoscaled_data)
    correlation_matrix = (nd_data.T @ nd_data) / (nd_data.shape[0])

    eigenvalues, vectors = np.linalg.eig(correlation_matrix)

    sorted_eigenvalue_vector_pairs: List[
        Tuple[float, NDArray[np.float64]]
    ] = sorted(zip(eigenvalues, vectors), key=lambda e: e[0], reverse=True)

    return PCAResutsView(
        autoscaled_data,
        nd_data,
        sorted_eigenvalue_vector_pairs,
        correlation_matrix,
    )


@dataclass
class PCAResutsView:

    autoscaled_data: Tuple[RecordBase]
    nd_data: NDArray[np.float64]
    eigenvalue_vector_pairs: List[Tuple[float, NDArray[np.float64]]]
    correlation_matrix: NDArray[np.float64]

    @property
    def eigenvalues(self) -> Tuple[float, ...]:
        return tuple(l for l, _ in self.eigenvalue_vector_pairs)

    @property
    def vectors(self) -> Tuple[NDArray[np.float64], ...]:
        return tuple(v for _, v in self.eigenvalue_vector_pairs)

    @property
    def percent_eigenvalues(self) -> Tuple[float, ...]:
        return tuple(v / self.column_number for v in self.eigenvalues)

    @property
    def cumulative_percent_lambdas(self) -> NDArray[np.float64]:
        return np.cumsum(self.percent_eigenvalues)

    @property
    def row_number(self) -> int:
        return self.nd_data.shape[0]

    @property
    def column_number(self) -> int:
        return self.nd_data.shape[1]

    @property
    def lambdas_number(self) -> int:
        return len(self.eigenvalues)

    @property
    def records_class_name(self) -> str:
        assert len(self.autoscaled_data) >= 1, "PCAResultView is empty."
        return self.autoscaled_data[0].class_name()

    def _common_plt(self, x: List[float], lambdas: Tuple[float, ...]):
        plt.plot(x, lambdas)
        plt.scatter(x, lambdas)
        plt.title(
            f"Scree plot for PCA on {self.row_number} "
            f"{self.records_class_name} objects"
        )
        plt.xlabel("Principal components")
        plt.grid(True)

    def scree_plot(self):
        x = np.arange(self.lambdas_number) + 1
        self._common_plt(x, self.eigenvalues)
        plt.ylabel("λ (eigenvalue)")
        plt.xticks(x, [f"PC{i}" for i in x])

    def percent_scree_plot(self):
        x = np.arange(self.lambdas_number) + 1
        percent_lambdas = self.percent_eigenvalues
        self._common_plt(x, percent_lambdas)
        plt.ylabel("% of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [f"PC{i}" for i in x])

    def cumulative_percent_scree_plot(self):
        x = np.arange(self.lambdas_number + 1)
        lambdas = np.concatenate(([0.0], self.cumulative_percent_lambdas))
        self._common_plt(x, lambdas)
        plt.ylabel("Cumulative % of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [""] + [f"PC{i}" for i in x[1:]])

    def subview(
        self, eigenvalue_vector_pairs: List[Tuple[float, NDArray[np.float64]]]
    ) -> "PCAResutsView":
        return PCAResutsView(
            self.autoscaled_data,
            self.nd_data,
            eigenvalue_vector_pairs,
            self.correlation_matrix,
        )

    def from_kaiser_criteria(self, treshold: float = 0.95):
        return self.subview(
            [(e, v) for e, v in self.eigenvalue_vector_pairs if e > treshold]
        )

    def from_total_variance_explained(self, minimal_percent: float = 0.70):
        lambdas = []
        for cumulated, ob in zip(
            self.cumulative_percent_lambdas, self.eigenvalue_vector_pairs
        ):
            if cumulated > minimal_percent:
                lambdas.append(ob)
                break
            else:
                lambdas.append(ob)
        return self.subview(
            lambdas,
        )

    def from_first_top(self, number: float = 2):
        return self.subview(
            self.eigenvalue_vector_pairs[:number],
        )

    @property
    def loads_matrix(self):
        return np.stack(self.vectors)

    @property
    def transformed_matrix(self):
        return (self.nd_data @ self.loads_matrix.T).T

    def principal_component_grid(
        self, point_size: int = 6, color: str = "b"
    ) -> Tuple[Figure, Axes]:
        fig, axes = plt.subplots(self.lambdas_number, self.lambdas_number - 1)

        i = 0
        for i, pci in enumerate(self.transformed_matrix):
            j = 0
            for k, pcj in enumerate(self.transformed_matrix):
                if k != i:
                    ax: plt.Axes = axes[i][j]  # type: ignore
                    ax.scatter(pci, pcj, s=point_size, color=color)
                    print(i, j)
                    ax.set_xlabel(f"PC{k}")
                    ax.set_ylabel(f"PC{i}")
                    j += 1

        return fig, axes
