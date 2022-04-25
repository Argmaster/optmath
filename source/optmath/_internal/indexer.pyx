# distutils: language = c++
# cython: language_level=3

from libcpp.vector cimport vector

from .ndindex cimport NDIndex


cdef class Index:
    cdef NDIndex _index

    def __cinit__(self, shape_: list | tuple):
        self._index = NDIndex(shape_)

    def __getitem__(self, index: int):
        max_index = self._index.size()
        if index >= max_index or index < 0:
            raise IndexError(
                f"Index out of bounds: got {index}, max {max_index}, min 0")
        return self._index.get(index)

    def __len__(self):
        return self._index.size()

    def __eq__(self, other: Index):
        return self._index == other._index

    def __ne__(self, other: Index):
        return self._index != other._index

    # def __iter__(self):
    #     return self._index.begin()
