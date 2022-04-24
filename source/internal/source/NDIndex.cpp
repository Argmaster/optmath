#include "NDIndex.h"

namespace optmath {
    /**
     * @brief Construct a new NDIndex::NDIndex object
     *
     * @param shape_ shape initializer to store
     */
    NDIndex::NDIndex(const std::initializer_list<index_t>& shape_)
        : nd_value(shape_) {
        assert(std::all_of(shape_.begin(), shape_.end(),
                           [](index_t i) { return i >= 0; }));
    }
    /**
     * @brief Copy underlying std::vector
     *
     * @param other indexer to copy values from
     * @return NDIndex& this
     */
    NDIndex::NDIndex(const NDIndex& other)
        : nd_value(other.nd_value) {}
    /**
     * @brief Copy underlying std::vector
     *
     * @param other indexer to copy values from
     * @return NDIndex& this
     */
    NDIndex& NDIndex::operator=(const NDIndex& other) {
        if (this != &other) {
            this->nd_value = other.nd_value;
            assert(this->nd_value.size() == other.nd_value.size());
        }
        return *this;
    }
    /**
     * @brief Move underlying std::vector
     *
     * @param other indexer to take ownership from
     * @return NDIndex& this
     */
    NDIndex::NDIndex(NDIndex&& other)
        : nd_value(std::move(other.nd_value)) {
        assert(other.nd_value.size() == 0);
    }
    /**
     * @brief Move underlying std::vector
     *
     * @param other indexer to take ownership from
     * @return NDIndex& this
     */
    NDIndex& NDIndex::operator=(NDIndex&& other) {
        if (this != &other) {
            this->nd_value = std::move(other.nd_value);
            assert(other.nd_value.size() == 0);
        }
        return *this;
    };
    /**
     * @brief Acquire index in nth dimension.
     *
     * @param __i index of dimension
     * @return index_t& indexer
     */
    index_t NDIndex::operator[](std::size_t __i) {
        return nd_value[__i];
        ;
    }
    /**
     * @brief Acquire number of dimensions.
     *
     * @return std::size_t
     */
    std::size_t NDIndex::size() const {
        return nd_value.size();
    }
    /**
     * @brief Common forward iterator begin.
     *
     * @return __shape_vector::iterator
     */
    __shape_vector::iterator NDIndex::begin() {
        return nd_value.begin();
    }
    /**
     * @brief Common forward iterator end
     *
     * @return __shape_vector::iterator
     */
    __shape_vector::iterator NDIndex::end() {
        return nd_value.end();
    }
    /**
     * @brief Constant forward iterator
     *
     * @return __shape_vector::const_iterator
     */
    __shape_vector::const_iterator NDIndex::cbegin() const {
        return nd_value.cbegin();
    }
    /**
     * @brief Constant forward iterator
     *
     * @return __shape_vector::const_iterator
     */
    __shape_vector::const_iterator NDIndex::cend() const {
        return nd_value.cend();
    }
    /**
     * @brief Constant reverse iterator
     *
     * @return __shape_vector::const_iterator
     */
    __shape_vector::const_reverse_iterator NDIndex::crbegin() const {
        return nd_value.crbegin();
    }
    /**
     * @brief Constant reverse iterator
     *
     * @return __shape_vector::const_iterator
     */
    __shape_vector::const_reverse_iterator NDIndex::crend() const {
        return nd_value.crend();
    }
    /**
     * @brief Compare equality of two indexers.
     *
     * @param lhs left operand
     * @param rhs right operand
     * @return true when both size and all values of indexers are equal
     * @return false when any of conditions is not met.
     */
    bool operator==(const NDIndex& lhs, const NDIndex& rhs) {
        if (lhs.size() == rhs.size()) {
            auto lhsb = lhs.cbegin();
            auto rhsb = rhs.cbegin();
            auto lhse = lhs.cend();
            auto rhse = rhs.cend();

            while (lhsb != lhse && rhsb != rhse) {
                auto left  = *lhsb;
                auto right = *rhsb;
                if (left != right)
                    return false;
                lhsb++;
                rhsb++;
            }
            return true;
        }
        return false;
    }
    /**
     * @brief Exact oposite of operator==.
     *
     * @param lhs left operand
     * @param rhs right operand
     * @return true when either size or any values of indexers are different.
     * @return false
     */
    bool operator!=(const NDIndex& lhs, const NDIndex& rhs) {
        return !(lhs == rhs);
    }
    /**
     * @brief C++ std::out << NDIndex(); compatibility.
     *
     * @param out stream to write to
     * @param other indexer to stringify
     * @return std::ostream& stream for chaining
     */
    std::ostream& operator<<(std::ostream& out, const NDIndex& other) {
        for (auto i = other.cbegin(); i != other.cend(); i++) {
            out << '[' << *i << ']';
        }
        return out;
    }

} // namespace optmath
