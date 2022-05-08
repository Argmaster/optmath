from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .. import RecordBase, to_numpy_array

TableOfFloatAndNDArray = Tuple[Tuple[float, NDArray[np.float64]], ...]


def PCA(autoscaled_data: Tuple[RecordBase]) -> "PCAResutsView":
    nd_data = to_numpy_array(autoscaled_data)
    correlation_matrix = (nd_data.T @ nd_data) / (nd_data.shape[0])

    eigenvalues, vectors = np.linalg.eig(correlation_matrix)

    sorted_eigenvalue_vector_pairs: TableOfFloatAndNDArray = tuple(
        sorted(
            zip(eigenvalues, vectors),
            key=lambda e: e[0],
            reverse=True,
        )
    )

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
    eigenvalue_vector_pairs: TableOfFloatAndNDArray
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

    def _common_plt(self, x: List[float], lambdas: Tuple[float, ...]) -> None:
        plt.plot(x, lambdas)
        plt.scatter(x, lambdas)
        plt.title(
            f"Scree plot for PCA on {self.row_number} "
            f"{self.records_class_name} objects"
        )
        plt.xlabel("Principal components")
        plt.grid(True)

    def scree_plot(self) -> None:
        x = np.arange(self.lambdas_number) + 1
        self._common_plt(x, self.eigenvalues)
        plt.ylabel("λ (eigenvalue)")
        plt.xticks(x, [f"PC{i}" for i in x])

    def percent_scree_plot(self) -> None:
        x = np.arange(self.lambdas_number) + 1
        percent_lambdas = self.percent_eigenvalues
        self._common_plt(x, percent_lambdas)
        plt.ylabel("% of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [f"PC{i}" for i in x])

    def cumulative_percent_scree_plot(self) -> None:
        x = np.arange(self.lambdas_number + 1)
        lambdas = np.concatenate(([0.0], self.cumulative_percent_lambdas))
        self._common_plt(x, lambdas)
        plt.ylabel("Cumulative % of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [""] + [f"PC{i}" for i in x[1:]])

    def subview(
        self,
        eigenvalue_vector_pairs: TableOfFloatAndNDArray,
    ) -> "PCAResutsView":
        return PCAResutsView(
            self.autoscaled_data,
            self.nd_data,
            eigenvalue_vector_pairs,
            self.correlation_matrix,
        )

    def from_kaiser_criteria(self, treshold: float = 0.95) -> "PCAResutsView":
        return self.subview(
            tuple(
                (e, v) for e, v in self.eigenvalue_vector_pairs if e > treshold
            )
        )

    def from_total_variance_explained(
        self, minimal_percent: float = 0.70
    ) -> "PCAResutsView":
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
            tuple(lambdas),
        )

    def from_first_top(self, number: int = 2) -> "PCAResutsView":
        return self.subview(
            self.eigenvalue_vector_pairs[:number],
        )

    def nth_view(self, number: int = 0) -> "PCAResutsView":
        return self.subview(
            (self.eigenvalue_vector_pairs[number],),
        )

    @property
    def loads_matrix(self) -> NDArray[np.float64]:
        return np.stack(self.vectors)

    @property
    def transformed_matrix(self) -> NDArray[np.float64]:
        return (self.nd_data @ self.loads_matrix.T).T

    def principal_component_grid(  # noqa CCR001
        self,
        point_size: int = 6,
        color: str = "b",
        grid: bool = True,
    ) -> Tuple[Figure, Axes]:
        assert (
            self.lambdas_number > 1
        ), "At least two components are required create plot."

        transformed = self.transformed_matrix
        grid_size = len(transformed) // 2
        fig, axes = plt.subplots(grid_size, grid_size + len(transformed) % 2)

        if len(transformed) == 2:
            axes = ((axes,),)
        elif len(transformed) == 3:
            axes = axes.reshape(1, 2)

        length = len(transformed)

        row_i = 0
        row_j = 0
        for even in range(0, length, 2):
            for odd in range(1, length, 2):

                ax: plt.Axes = axes[row_i][row_j]  # type: ignore
                ax.scatter(
                    transformed[even],
                    transformed[odd],
                    s=point_size,
                    color=color,
                    alpha=0.5,
                )
                if grid:
                    ax.grid(linestyle="--")
                ax.set_xlabel(f"PC{even + 1}")
                ax.set_ylabel(f"PC{odd + 1}")

                if row_i < grid_size - 1:
                    row_i += 1
                else:
                    row_i = 0
                    row_j += 1

        return fig, axes

    def loads_grid(
        self, grid: bool = True, limit_lines: float = 0.7
    ) -> Tuple[Figure, Axes]:
        loads = self.loads_matrix

        x_values = np.arange(len(loads[0]))
        x_values_ex = np.arange(-1, len(loads[0]) + 1)

        fig, axes = plt.subplots(len(loads))  # type: ignore

        if len(loads) == 1:
            axes = (axes,)  # type: ignore

        axes: Tuple[Axes, ...]

        for i, (vector, ax) in enumerate(zip(loads, axes)):

            if limit_lines is not None:
                ax.fill_between(
                    x_values_ex,
                    [limit_lines] * len(x_values_ex),
                    [-limit_lines] * len(x_values_ex),
                    color="#1574b340",
                )
            if grid:
                ax.grid(axis="y", linestyle="--")
            ax.bar(x_values, vector)
            ax.set_xlim([min(x_values_ex), max(x_values_ex)])
            ax.set_ylim([-1.0, 1.0])
            ax.set_title(f"PC{i + 1} loadings")
            ax.set_xlabel(f"PC{i + 1}")
            ax.set_ylabel("Eigenvalue")
            columns = self.autoscaled_data[0].columns()
            ax.set_xticks(x_values, columns[1:], rotation=45, ha="right")

        return fig, axes
