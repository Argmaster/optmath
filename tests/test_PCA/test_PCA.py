from dataclasses import dataclass
from pathlib import Path

import pandas
from matplotlib import pyplot as plt

from optmath import RecordBase, autoscale
from optmath.PCA import PCA


@dataclass(frozen=True)
class PumpkinSeed(RecordBase):
    Area: float
    Perimeter: float
    Major_Axis_Length: float
    Minor_Axis_Length: float
    Solidity: float
    Roundness: float


TEST_PCA_DIR = Path(__file__).parent


def test_PCA_correlation_matrix():
    raw = pandas.read_csv(TEST_PCA_DIR / "data" / "test_seeds.csv").to_numpy()
    raw = autoscale(raw)
    data = PumpkinSeed.new(raw)
    algorithm = PCA(data)
    algorithm.execute()
    algorithm.scree_plot()
    plt.show()
    algorithm.percent_scree_plot()
    plt.show()
    algorithm.cumulative_percent_scree_plot()
    plt.show()
