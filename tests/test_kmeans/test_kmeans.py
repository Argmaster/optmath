from dataclasses import dataclass

import numpy as np

from optmath import PCAResutsView, RecordBase
from optmath.Kmeans import Kmeans

from ..test_PCA.test_PCA import pca_seeds_view  # noqa


@dataclass(frozen=True)
class PostPCASeed(RecordBase):
    pc1: float
    pc2: float
    pc3: float


class TestKmeans:
    def test_kmeans_simple_pumpkin_data(
        self, pca_seeds_view: PCAResutsView  # noqa
    ):
        np.random.seed(0)
        subview = pca_seeds_view.get_view_from_first_top(3)
        data = PostPCASeed.new(subview.get_post_transfrom())
        Kmeans(data, cluster_count=4)
