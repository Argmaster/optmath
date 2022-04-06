from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from optmath.HCA import (
    HCA,
    Cluster,
    CompleteLinkage,
    Euclidean,
    HCAStep,
    RecordBase,
)
from optmath.HCA.record import autoscale
from scipy.cluster import hierarchy


@dataclass(frozen=True)
class Seed(RecordBase):
    size: float
    quality: float


raw = [
    [2, 3],
    [3, 8],
    [4, 7],
    [1, 1],
    [0, 0],
]

clusters = Cluster.new(Seed.new(raw))


def test_HCA():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    algorithm.reduce()


def test_HCA_iteration():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    for step in algorithm:
        assert isinstance(step, HCAStep)
    print(algorithm.last)


def test_HCA_result():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    assert str(algorithm.result()) == "Cluster(ID=8,s=5,h=8.544)"


def test_HCA_dendrogram():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    cluster = algorithm.result()

    buffer_custom = BytesIO()
    z = cluster.Z()
    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.savefig(buffer_custom, format="png")

    buffer_scipy = BytesIO()
    z = hierarchy.linkage(raw, "complete")
    print(z)
    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.savefig(buffer_scipy, format="png")

    assert buffer_custom.read() == buffer_scipy.read()


def test_HCA_dendrogram_show():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    cluster = algorithm.result()

    z = cluster.Z()
    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.show()


@dataclass(frozen=True)
class PumpkinSeed(RecordBase):
    Area: float
    Perimeter: float
    Major_Axis_Length: float
    Minor_Axis_Length: float
    Solidity: float
    Roundness: float


TEST_HCA_DIR = Path(__file__).parent


def test_HCA_complex_pumpkin_data():
    raw = pd.read_csv(TEST_HCA_DIR / "data" / "test_seeds.csv").to_numpy()
    raw = autoscale(raw)
    clusters = Cluster.new(PumpkinSeed.new(autoscale(raw)))
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    cluster = algorithm.result()
    z = cluster.Z()

    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.show()
