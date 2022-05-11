from dataclasses import dataclass
from pathlib import Path

import pandas
import pytest

from optmath import RecordBase, autoscale
from optmath.PCA import PCA, PCAResutsView


@dataclass(frozen=True)
class PumpkinSeed(RecordBase):
    Area: float
    Perimeter: float
    Major_Axis_Length: float
    Minor_Axis_Length: float
    Convex_Area: int
    Equiv_Diameter: float
    Eccentricity: float
    Solidity: float
    Extent: float
    Roundness: float
    Aspect_Ration: float
    Compactness: float
    Class: str


TEST_PCA_DIR = Path(__file__).parent


@pytest.fixture()
def pca_seeds_view() -> PCAResutsView:
    raw = pandas.read_csv(TEST_PCA_DIR / "data" / "test_seeds.csv").to_numpy()
    raw = autoscale(raw)
    data = PumpkinSeed.new(raw)
    return PCA(data)


class TestPCAResultView:
    def test_scree_plot(self, pca_seeds_view: PCAResutsView):
        pca_seeds_view.show_scree_plot()

    def test_percent_scree_plot(self, pca_seeds_view: PCAResutsView):
        pca_seeds_view.show_percent_scree_plot()

    def test_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutsView
    ):
        pca_seeds_view.show_cumulative_percent_scree_plot()

    def test_from_kaiser_criteria_scree_plot(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_kaiser_criteria(0.95)
        view.show_scree_plot()

    def test_from_kaiser_criteria_percent_scree_plot(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_kaiser_criteria(0.95)
        view.show_percent_scree_plot()

    def test_from_kaiser_criteria_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_kaiser_criteria(0.95)
        view.show_cumulative_percent_scree_plot()

    def test_from_total_variance_explained_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_total_variance_explained(0.7)
        view.show_cumulative_percent_scree_plot()

    def test_principal_component_grid_four_components(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_first_top(4)
        fig, _ = view.show_principal_component_grid()
        fig.set_dpi(100)

    def test_principal_component_grid_three_components(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_first_top(3)
        fig, _ = view.show_principal_component_grid()
        fig.set_dpi(100)

    def test_principal_component_grid_two_components(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_first_top(2)
        fig, _ = view.show_principal_component_grid()
        fig.set_dpi(100)

    def test_principal_component_loads_grid(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_view_from_first_top(3)
        fig, _ = view.show_loads_grid()
        fig.set_size_inches(5, 10)
        fig.set_dpi(80)

    def test_principal_component_single_pc(
        self, pca_seeds_view: PCAResutsView
    ):
        view = pca_seeds_view.get_nth_view(2)
        fig, _ = view.show_loads_grid(limit=0.5)
        fig.set_size_inches(5, 10)
        fig.set_dpi(80)
