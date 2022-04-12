#pragma once
#include <algorithm>
#include <boost/iterator/zip_iterator.hpp>
#include <cstdint>
#include <execution>
#include <numeric>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;

    class Shape {
        __shape_vector shape;

       public:
        Shape(const std::initializer_list<int64_t> &shape_) : shape(shape_) {}

        int64_t buffer_size() const {
            return std::reduce(
                std::execution::seq, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }
        int64_t operator[](std::size_t __i) const { return shape[__i]; }

        std::size_t size() const { return shape.size(); }
        std::vector<int64_t>::const_iterator cbegin() const {
            return shape.cbegin();
        }
        std::vector<int64_t>::const_iterator cend() const {
            return shape.cend();
        }

        friend bool operator==(const Shape &lhs, const Shape &rhs);
    };

    bool operator==(const Shape &lhs, const Shape &rhs) {
        auto lhsb = lhs.cbegin();
        auto rhsb = rhs.cbegin();
        auto lhse = lhs.cend();
        auto rhse = rhs.cend();

        if (lhs.size() == rhs.size()) {
            using __T = const boost::tuple<const double &, const int &> &;
            bool result = true;
            std::for_each(
                boost::make_zip_iterator(boost::make_tuple(lhsb, rhsb)),
                boost::make_zip_iterator(boost::make_tuple(lhse, rhse)),
                [&result](__T item) -> void {
                    result = result && (item.get<0>() == item.get<1>());
                });
            return result;
        }
        return false;
    }

}  // namespace optmath
