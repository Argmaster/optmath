#include "NDShape.h"

namespace optmath {
    /**
     * @brief Construct a new NDShape object
     *
     * @param shape_ initial shape
     */
    NDShape::NDShape(const std::initializer_list<shape_t>& shape_)
        : NDIndex(shape_) {
        assert(std::all_of(shape_.begin(), shape_.end(),
                           [](index_t i) { return i > 0; }));
        // calculates and caches minimal buffer size required for
        // nd buffer with this shape
        nd_buffer_size = std::reduce(
            this->cbegin(), this->cend(), 1,
            [](shape_t first, shape_t second) { return first * second; });
    }
    /**
     * @brief Construct a new NDShape object, copy value from existing one
     *
     * @param other shape to copy from.
     */
    NDShape::NDShape(const NDShape& other)
        : NDIndex(other) {
        nd_buffer_size = other.nd_buffer_size;
    }
    /**
     * @brief Copy NDShape value into this object
     *
     * @param other shape to copy
     * @return NDShape& this shape
     */
    NDShape& NDShape::operator=(const NDShape& other) {
        if (this != &other) {
            this->NDIndex::operator=(other);
            this->nd_buffer_size = other.nd_buffer_size;
        }
        return *this;
    }
    /**
     * @brief Move underlying std::vector to new NDShape
     *
     * @param other shape to take ownership from.
     * @return NDShape& this
     */
    NDShape::NDShape(NDShape&& other)
        : NDIndex(std::move(other)) {
        nd_buffer_size       = other.nd_buffer_size;
        other.nd_buffer_size = 0;
    };
    /**
     * @brief Move underlying std::vector
     *
     * @param other shape to take ownership from.
     * @return NDShape& this
     */
    NDShape& NDShape::operator=(NDShape&& other) {
        if (this != &other) {
            this->NDIndex::operator=(other);
            this->nd_buffer_size = other.nd_buffer_size;
            other.nd_buffer_size = 0;
        }
        return *this;
    }
    /**
     * @brief Get size of buffer required to contain tensor of this shape.
     *
     * @return std::size_t linear size of buffer.
     */
    std::size_t NDShape::buffer_size() const {
        return this->nd_buffer_size;
    }
    /**
     * @brief Calculates in buffer index of element pointed by NDIndex object.
     *
     * @param index Indexer object pointing to value in buffer.
     * @return std::size_t linear in buffer position.
     */
    std::size_t NDShape::in_buffer_position(const NDIndex& index) const {
        // size inequality is UB
        assert(index.size() == this->size());

        auto beginShape = this->crbegin();
        auto endShape   = this->crend();
        auto beginIndex = index.crbegin();
        auto endIndex   = index.crend();

        index_t position   = 0ULL;
        index_t multiplier = 1ULL;

        while (beginShape != endShape) {
            assert(beginIndex != endIndex);
            position += (*beginIndex) * multiplier;

            multiplier *= *beginShape;

            beginShape++;
            beginIndex++;
        }
        assert(position < this->buffer_size());
        assert(position >= 0);
        return position;
    }
    /**
     * @brief Common C++ string conversion support
     *
     * @param out stream to write to
     * @param other NDShape to serialize
     * @return std::ostream& stream for << chaining
     */
    std::ostream& operator<<(std::ostream& out, const NDShape& other) {
        auto begin = other.cbegin();
        auto end   = other.cend();

        out << '{';

        while (true) {
            out << *begin;
            begin++;
            if (begin == end) {
                break;
            }
            out << ',' << ' ';
        }
        out << '}';

        return out;
    }

} // namespace optmath
