import numpy as np

from optmath import Kohonen


class TestKohonen:
    def test_kohonen(self):
        np.random.seed(0)
        sample_data = np.random.normal(size=(10, 3))
        k_map = Kohonen(shape=32)
        k_map.execute(sample_data, 5)
