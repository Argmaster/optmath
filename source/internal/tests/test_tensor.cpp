#include <gtest/gtest.h>

#include "Tensor.h"

namespace optmath {

    class TensorTest : public ::testing::Test {};

    TEST_F(TensorTest, FromNDShapedCreation) {
        auto tensor = Tensor<int>({32, 32});
        ASSERT_EQ(tensor.shape(), NDShape({32, 32}));
    }

    TEST_F(TensorTest, ElementAccess) {
        auto tensor = Tensor<int>({4, 3, 5});
        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    tensor[{i, j, k}] = i * j * k;
                }
            }
        }
        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    auto test_val = tensor[{i, j, k}];
                    ASSERT_EQ(test_val, i * j * k);
                }
            }
        }

        ASSERT_EQ(tensor.shape(), NDShape({32, 32}));
    }
} // namespace optmath
