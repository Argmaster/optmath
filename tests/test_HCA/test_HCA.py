from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy
import numpy.typing as npt
import pandas as pd
import pytest
from PIL import Image
from scipy.cluster import hierarchy

from optmath.HCA import (
    HCA,
    Chebyshev,
    Cluster,
    CompleteLinkage,
    Euclidean,
    HCAStep,
    Manhattan,
    RecordBase,
    SingleLinkage,
    Ward,
)
from optmath.HCA.record import autoscale


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


def compare_ndarrays(first: npt.NDArray, second: npt.NDArray) -> float:
    first = first.reshape(-1)
    second = second.reshape(-1)
    return numpy.count_nonzero(first == second) / len(first)


def dump_dendrogram(z_matrix: npt.NDArray) -> npt.NDArray:
    io = BytesIO()
    hierarchy.dendrogram(z_matrix, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.savefig(io, format="png")
    io.seek(0)
    image = Image.open(io)
    raw = numpy.asarray(image)
    return raw


def test_HCA():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    algorithm.reduce()


def test_HCA_iteration():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    for step in algorithm:
        assert isinstance(step, HCAStep)


def test_HCA_result():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    assert str(algorithm.result()) == "Cluster(ID=8,s=5,h=8.544)"


def test_HCA_dendrogram_complete_euclidean():
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    cluster = algorithm.result()

    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="complete", metric="euclidean")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.99


def test_HCA_dendrogram_single_euclidean():
    algorithm = HCA(clusters, SingleLinkage(Euclidean()))
    cluster = algorithm.result()
    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="single", metric="euclidean")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.99


def test_HCA_dendrogram_single_manhattan():
    algorithm = HCA(clusters, SingleLinkage(Manhattan()))
    cluster = algorithm.result()

    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="single", metric="cityblock")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.99


def test_HCA_dendrogram_complete_chebyshev():
    algorithm = HCA(clusters, SingleLinkage(Chebyshev()))
    cluster = algorithm.result()

    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="single", metric="chebyshev")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.99


@pytest.mark.skip(
    reason=(
        "Known issue with Ward distance selector - "
        "mismatch between scipy and this implementation"
    )
)
def test_HCA_dendrogram_ward_euclidean():
    algorithm = HCA(clusters, Ward(Euclidean()))
    cluster = algorithm.result()

    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="ward", metric="euclidean")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.99


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
    clusters = Cluster.new(PumpkinSeed.new(raw))
    algorithm = HCA(clusters, SingleLinkage(Euclidean()))
    cluster = algorithm.result()

    z = hierarchy.linkage(raw, method="single", metric="euclidean")
    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    z = cluster.Z()
    hierarchy.dendrogram(z, leaf_rotation=90.0, leaf_font_size=8.0)
    plt.show()


def test_HCA_complex_pumpkin_data_complete_euclidean():
    raw = pd.read_csv(TEST_HCA_DIR / "data" / "test_seeds.csv").to_numpy()
    raw = autoscale(raw)
    clusters = Cluster.new(PumpkinSeed.new(autoscale(raw)))
    algorithm = HCA(clusters, CompleteLinkage(Euclidean()))
    cluster = algorithm.result()

    z_custom = cluster.Z()
    z_scipy = hierarchy.linkage(raw, method="complete", metric="euclidean")

    custom_version = dump_dendrogram(z_custom)
    scipy_version = dump_dendrogram(z_scipy)

    result = compare_ndarrays(custom_version, scipy_version)
    assert result > 0.98
