from libcpp cimport bool
from libcpp.vector cimport vector


cdef extern from "NDIndex.h" namespace "optmath":
    cdef cppclass NDIndex:
        NDIndex(const vector[long] & )
        NDIndex()

        long operator[](long)
        long get(long)

        vector[long].iterator               begin()
        vector[long].iterator               end()
        vector[long].const_iterator         cbegin() const
        vector[long].const_iterator         cend() const
        vector[long].const_reverse_iterator crbegin() const
        vector[long].const_reverse_iterator crend() const

        bool operator == (const NDIndex & )
        bool operator != (const NDIndex & )
        long size()
