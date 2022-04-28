from dataclasses import dataclass
from pathlib import Path

import pandas
import pytest

from optmath import RecordBase, autoscale
from optmath.PCA import PCA, PCAResutView


@dataclass(frozen=True)
class PumpkinSeed(RecordBase):
    Area: float
    Perimeter: float
    Major_Axis_Length: float
    Minor_Axis_Length: float
    Solidity: float
    Roundness: float


TEST_PCA_DIR = Path(__file__).parent


@pytest.fixture()
def pca_seeds_view() -> PCAResutView:
    raw = pandas.read_csv(TEST_PCA_DIR / "data" / "test_seeds.csv").to_numpy()
    raw = autoscale(raw)
    data = PumpkinSeed.new(raw)
    return PCA(data)


class TestPCAResultView:
    def test_scree_plot(self, pca_seeds_view: PCAResutView):
        pca_seeds_view.scree_plot()

    def test_percent_scree_plot(self, pca_seeds_view: PCAResutView):
        pca_seeds_view.percent_scree_plot()

    def test_cumulative_percent_scree_plot(self, pca_seeds_view: PCAResutView):
        pca_seeds_view.cumulative_percent_scree_plot()

    def test_from_kaiser_criteria_scree_plot(
        self, pca_seeds_view: PCAResutView
    ):
        view = pca_seeds_view.from_kaiser_criteria(0.95)
        view.scree_plot()
        ()

    def test_from_kaiser_criteria_percent_scree_plot(
        self, pca_seeds_view: PCAResutView
    ):
        view = pca_seeds_view.from_kaiser_criteria(0.95)
        view.percent_scree_plot()

    def test_from_kaiser_criteria_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutView
    ):
        view = pca_seeds_view.from_kaiser_criteria(0.95)
        view.cumulative_percent_scree_plot()

    def test_from_total_variance_explained_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutView
    ):
        view = pca_seeds_view.from_total_variance_explained(0.7)
        view.cumulative_percent_scree_plot()

    def test_from_first_top_cumulative_percent_scree_plot(
        self, pca_seeds_view: PCAResutView
    ):
        view = pca_seeds_view.from_first_top(3)
        fig, _ = view.principal_component_grid()
        fig.set_size_inches(16, 16)
        fig.set_dpi(100)
