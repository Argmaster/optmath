#include <gtest/gtest.h>

#include "Tensor.h"

namespace optmath {

    class TensorTest : public ::testing::Test {};

    TEST_F(TensorTest, FromNDShapedCreation) {
        auto tensor = Tensor<int>({32, 32});
        ASSERT_EQ(tensor.shape(), NDShape({32, 32}));
    }


}
