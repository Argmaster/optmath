from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .. import RecordBase, to_numpy_array

TableOfFloatAndNDArray = Tuple[Tuple[float, NDArray[np.float64]], ...]


def PCA(autoscaled_data: Tuple[RecordBase, ...]) -> "PCAResutsView":
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

    autoscaled_data: Tuple[RecordBase, ...]
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

    def _common_plt_ops(
        self, x: List[float], lambdas: Tuple[float, ...]
    ) -> None:
        plt.plot(x, lambdas)
        plt.scatter(x, lambdas)
        plt.title(
            f"Scree plot for PCA on {self.row_number} "
            f"{self.records_class_name} objects"
        )
        plt.xlabel("Principal components")
        plt.grid(True)

    def show_scree_plot(self) -> None:
        x = np.arange(self.lambdas_number) + 1
        self._common_plt_ops(x, self.eigenvalues)
        plt.ylabel("λ (eigenvalue)")
        plt.xticks(x, [f"PC{i}" for i in x])

    def show_percent_scree_plot(self) -> None:
        x = np.arange(self.lambdas_number) + 1
        percent_lambdas = self.percent_eigenvalues
        self._common_plt_ops(x, percent_lambdas)
        plt.ylabel("% of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [f"PC{i}" for i in x])

    def show_cumulative_percent_scree_plot(self) -> None:
        x = np.arange(self.lambdas_number + 1)
        lambdas = np.concatenate(([0.0], self.cumulative_percent_lambdas))
        self._common_plt_ops(x, lambdas)
        plt.ylabel("Cumulative % of variance explained")
        y = np.linspace(0, 1.0, 11)
        plt.yticks(y, [f"{f*100:.1f}%" for f in y])
        plt.xticks(x, [""] + [f"PC{i}" for i in x[1:]])

    def get_view(
        self,
        eigenvalue_vector_pairs: TableOfFloatAndNDArray,
    ) -> "PCAResutsView":
        return PCAResutsView(
            self.autoscaled_data,
            self.nd_data,
            eigenvalue_vector_pairs,
            self.correlation_matrix,
        )

    def get_view_from_kaiser_criteria(
        self, treshold: float = 0.95
    ) -> "PCAResutsView":
        return self.get_view(
            tuple(
                (e, v) for e, v in self.eigenvalue_vector_pairs if e > treshold
            )
        )

    def get_view_from_total_variance_explained(
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
        return self.get_view(
            tuple(lambdas),
        )

    def get_view_from_first_top(self, number: int = 2) -> "PCAResutsView":
        return self.get_view(
            self.eigenvalue_vector_pairs[:number],
        )

    def get_nth_view(self, number: int = 0) -> "PCAResutsView":
        return self.get_view(
            (self.eigenvalue_vector_pairs[number],),
        )

    @property
    def loads_matrix(self) -> NDArray[np.float64]:
        return np.stack(self.vectors)

    @property
    def transformed_matrix(self) -> NDArray[np.float64]:
        return (self.nd_data @ self.loads_matrix.T).T

    def show_principal_component_grid(  # noqa CCR001
        self,
        point_size: int = 6,
        color: str = "b",
        grid: bool = True,
    ) -> Tuple[Figure, Axes]:
        assert (
            self.lambdas_number > 1
        ), "At least two components are required create plot."

        transformed = self.transformed_matrix
        grid_size = len(transformed)
        fig, axes = plt.subplots(grid_size, grid_size)

        if len(transformed) == 2:
            axes = ((axes,),)

        for (i, pci), ax_row in zip(enumerate(transformed), axes):
            for (j, pcj), ax in zip(enumerate(transformed), ax_row):

                ax.scatter(
                    pci,
                    pcj,
                    s=point_size,
                    color=color,
                    alpha=0.5,
                )
                if grid:
                    ax.grid(linestyle="--")
                ax.set_xlabel(f"PC{i + 1}")
                ax.set_ylabel(f"PC{j + 1}")

        return fig, axes

    def show_loads_grid(  # noqa: CCR001
        self, grid: bool = True, limit: float = 0.7
    ) -> Tuple[Figure, Tuple[Axes, ...]]:
        loads = self.loads_matrix

        x_values = np.arange(len(loads[0]))
        x_values_ex = np.arange(-1, len(loads[0]) + 1)

        fig, axes = plt.subplots(len(loads))  # type: ignore

        if len(loads) == 1:
            axes = (axes,)  # type: ignore

        axes: Tuple[Axes, ...]

        for i, (vector, ax) in enumerate(zip(loads, axes)):

            if limit is not None:
                ax.fill_between(
                    x_values_ex,
                    [limit] * len(x_values_ex),
                    [-limit] * len(x_values_ex),
                    color="#1574b340",
                )
            if grid:
                ax.grid(axis="y", linestyle="--")
            bars = ax.bar(x_values, vector)
            for patch, height in zip(bars, vector):
                if abs(height) >= limit:
                    patch.set_color("#32a852")
            ax.set_xlim([min(x_values_ex), max(x_values_ex)])
            ax.set_ylim([-1.0, 1.0])
            ax.set_title(f"PC{i + 1} loadings")
            ax.set_xlabel(f"PC{i + 1}")
            ax.set_ylabel("Eigenvalue")
            columns = self.autoscaled_data[0].columns_numeric()
            ax.set_xticks(x_values, columns[1:], rotation=45, ha="right")

        return fig, axes
