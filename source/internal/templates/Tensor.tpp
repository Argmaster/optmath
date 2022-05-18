#pragma once

#include "Tensor.h"

#define TENSOR_METHOD(return_type)                                            \
    TENSOR_TEMPLATE return_type Tensor<TENSOR_VAL_T>::

#define NDBUFFER_T Tensor<TENSOR_VAL_T>

namespace optmath {
    /**
     * @brief Construct a new Tensor object with given shape
     *
     * @param shape_
     */
    TENSOR_METHOD()
    Tensor(const NDShape& shape_)
        : nd_buffer(shape_) {
        assert(shape_.size() != 0);
        assert(this->begin() != nullptr);
    }
    /**
     * @brief Construct a new Tensor without initialization
     *
     */
    TENSOR_METHOD()
    Tensor() {}
    /**
     * @brief Return current shape of tensor.
     *
     * @return const NDShape&
     */
    TENSOR_METHOD(const NDShape&) shape() const {
        return this->nd_buffer.shape();
    }
    /**
     * @brief Set value at position.
     */
    TENSOR_METHOD(void) Set(const NDIndex& nd_indexer, TENSOR_VAL_T& new_value) {
        this->nd_buffer[nd_indexer] = new_value;
    }
    /**
     * @brief Get element from position.
     */
    TENSOR_METHOD(TENSOR_VAL_T&) Get(const NDIndex& nd_indexer) {
        return this->nd_buffer[nd_indexer];
    }
    /**
     * @brief Return begin iterator for tensor.
     *
     * @return TENSOR_VAL_T*
     */
    TENSOR_METHOD(TENSOR_VAL_T*) begin() {
        return this->nd_buffer.begin();
    }
    /**
     * @brief Return end iterator sentinel for tensor.
     *
     * @return TENSOR_VAL_T*
     */
    TENSOR_METHOD(TENSOR_VAL_T*) end() {
        return this->nd_buffer.end();
    }
    /**
     * @brief Return constant begin iterator for tensor.
     *
     * @return const TENSOR_VAL_T*
     */
    TENSOR_METHOD(const TENSOR_VAL_T*) cbegin() const {
        return this->nd_buffer.cbegin();
    }
    /**
     * @brief Return constant end iterator sentinel for tensor.
     *
     * @return const TENSOR_VAL_T*
     */
    TENSOR_METHOD(const TENSOR_VAL_T*) cend() const {
        return this->nd_buffer.cend();
    }
    /**
     * @brief Access single element from tensor.
     *
     * @param index n-dimensional index pointing to element
     * @return T& in buffer element reference
     */
    TENSOR_METHOD(TENSOR_VAL_T&) operator[](const NDIndex& nd_indexer) {
        return this->Get(nd_indexer);
    }
    /**
     * @brief Compare two Tensor instances.
     *
     * @param other
     * @return true for identical tensors or same tensor.
     */
    TENSOR_METHOD(bool) operator==(const Tensor& other) const {
        return this->nd_buffer == other.nd_buffer;
    }
    /**
     * @brief C++ std::out << NDBuffer(); compatibility.
     *
     * @param out stream to write to
     * @param other buffer to stringify
     * @return std::ostream& stream for chaining
     */
    TENSOR_METHOD(std::ostream&) to_stream(std::ostream& stream) const {
        assert(this->nd_buffer.cbegin() != nullptr);
        auto begin = this->cbegin();
        auto end   = this->cend();

        switch (this->shape().size()) {
        case 0: {
            stream << "[]";
            break;
        }
        case 1: {
            this->nd_buffer.to_stream(stream);
            break;
        }

        default: {
            this->nd_buffer.to_stream(stream);
            break;
        }
        }

        return stream;
    }
    /**
     * @brief String representation of tensor instance.
     *
     * @return std::string tensor representation
     */
    TENSOR_METHOD(std::string) to_string() const {
        std::stringstream ss;
        this->to_stream(ss);
        return ss.str();
    }
} // namespace optmath
