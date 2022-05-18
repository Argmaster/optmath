from libcpp.vector cimport vector

from .ndindex cimport NDIndex


cdef extern from "NDShape.h" namespace "optmath":
    cdef cppclass NDShape(NDIndex):
        NDShape(const vector[long] &)
        NDShape()
