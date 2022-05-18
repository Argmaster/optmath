#include <gtest/gtest.h>

#include "Tensor.h"

namespace optmath {

    class TensorTest : public ::testing::Test {};

    TEST_F(TensorTest, TensorCreation1D) {
        auto tensor = Tensor<int64_t>({32});
        ASSERT_EQ(tensor.shape(), NDShape({32}));
    }
    TEST_F(TensorTest, TensorCreation2D) {
        auto tensor = Tensor<int64_t>({32, 54});
        ASSERT_EQ(tensor.shape(), NDShape({32, 54}));
    }
    TEST_F(TensorTest, TensorCreation3D) {
        auto tensor = Tensor<int64_t>({32, 54, 5});
        ASSERT_EQ(tensor.shape(), NDShape({32, 54, 5}));
    }
    TEST_F(TensorTest, TensorCreation4D) {
        auto tensor = Tensor<int64_t>({9, 3, 5, 7});
        ASSERT_EQ(tensor.shape(), NDShape({9, 3, 5, 7}));
    }
    TEST_F(TensorTest, TensorCreation5D) {
        auto tensor = Tensor<int64_t>({9, 3, 5, 7, 2});
        ASSERT_EQ(tensor.shape(), NDShape({9, 3, 5, 7, 2}));
    }
    TEST_F(TensorTest, ElementAccess3D) {
        auto tensor = Tensor<int64_t>({4, 3, 5});

        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    tensor[{i, j, k}] = i + j + k;
                }
            }
        }
        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    auto test_val = tensor[{i, j, k}];
                    std::cout << NDIndex({i, j, k}) << " " << test_val
                              << std::endl;
                    ASSERT_EQ(test_val, i + j + k);
                }
            }
        }
    }
    TEST_F(TensorTest, StringifyToStream) {
        auto first = TensorInt32({3, 2});

        auto j = 0;
        for (auto& i : first) {
            i = j;
            j++;
        }
        std::stringstream ss;
        ss << first;
        auto str = ss.str();
        ASSERT_STREQ("[0, 1, 2, 3, 4, 5]", str.c_str());
    }
    TEST_F(TensorTest, StringifyToString) {
        auto first = TensorInt32({3, 2});

        auto j = 0;
        for (auto& i : first) {
            i = j;
            j++;
        }
        auto s = first.to_string();
        ASSERT_STREQ("[0, 1, 2, 3, 4, 5]", s.c_str());
    }
} // namespace optmath
