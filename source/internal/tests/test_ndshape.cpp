#include <gtest/gtest.h>

#include "NDShape.h"

namespace optmath {
    class NDShapeTest : public ::testing::Test {};

    TEST_F(NDShapeTest, NDShape3D) {
        auto test_shape = optmath::NDShape{2, 1, 4};
        ASSERT_EQ(test_shape[0], 2);
        ASSERT_EQ(test_shape[1], 1);
        ASSERT_EQ(test_shape[2], 4);
        ASSERT_EQ(test_shape.size(), 3);
    }
    TEST_F(NDShapeTest, CopyConstruction) {
        auto test_index = optmath::NDShape({2, 1, 4});
        {
            auto test_index_copy{test_index};
            ASSERT_EQ(test_index_copy.buffer_size(), test_index.buffer_size());
        }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }
    TEST_F(NDShapeTest, CopyAssignment) {
        auto test_index = optmath::NDShape({2, 1, 4});
        {
            optmath::NDShape test_index_copy{3, 3};
            ASSERT_EQ(test_index_copy[0], 3);
            ASSERT_EQ(test_index_copy[1], 3LL);
            test_index_copy = test_index;
            ASSERT_EQ(test_index_copy[0], 2LL);
            ASSERT_EQ(test_index_copy[1], 1LL);
            ASSERT_EQ(test_index_copy[2], 4LL);
            ASSERT_EQ(test_index_copy.buffer_size(), test_index.buffer_size());
        }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }
    TEST_F(NDShapeTest, MoveConstruction) {
        auto test_index_copy{std::move(optmath::NDShape({2, 1, 4}))};
        ASSERT_EQ(test_index_copy[0], 2LL);
        ASSERT_EQ(test_index_copy[1], 1LL);
        ASSERT_EQ(test_index_copy[2], 4LL);
    }
    TEST_F(NDShapeTest, MoveAssignment) {
        optmath::NDShape test_index_copy{3, 3};
        ASSERT_EQ(test_index_copy[0], 3);
        ASSERT_EQ(test_index_copy[1], 3LL);
        auto second     = optmath::NDShape({2, 1, 4});
        auto old_size   = second.buffer_size();
        test_index_copy = std::move(second);
        ASSERT_EQ(test_index_copy[0], 2LL);
        ASSERT_EQ(test_index_copy[1], 1LL);
        ASSERT_EQ(test_index_copy[2], 4LL);
        ASSERT_EQ(test_index_copy.buffer_size(), old_size);
    }
    TEST_F(NDShapeTest, BufferSize3D) {
        auto test_shape = optmath::NDShape{2, 1, 4};
        ASSERT_EQ(test_shape.buffer_size(), 8);
    }
    TEST_F(NDShapeTest, BufferSize4D) {
        auto test_shape = optmath::NDShape{34, 12, 93, 43};
        ASSERT_EQ(test_shape.buffer_size(), 1631592);
    }
    TEST_F(NDShapeTest, NoNDShapeAssignment) {
        auto test_shape = optmath::NDShape{32, 6};
        // test_shape[0]   = 24; // should be compile error - uncomment for
        // manual check
    }
    TEST_F(NDShapeTest, InBufferPosition3DInBounds) {
        auto test_shape = optmath::NDShape{4, 5, 3};
        ASSERT_EQ(test_shape.in_buffer_position({1, 0, 1}), 16);
    }
    TEST_F(NDShapeTest, InBufferPosition3DOutOfBounds) {
        auto test_shape = optmath::NDShape{4, 5, 3};
        ASSERT_DEATH(test_shape.in_buffer_position({8, 0, 1}), "");
    }
    TEST_F(NDShapeTest, InBufferPosition3DIndexerMismatch) {
        auto test_shape_2 = optmath::NDShape{38, 11};
        ASSERT_DEATH(test_shape_2.in_buffer_position({1, 0, 1}), "");
    }
} // namespace optmath
