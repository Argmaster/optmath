#include <gtest/gtest.h>

#include "NDBuffer.h"

namespace optmath {

    class NDBufferTest : public ::testing::Test {};

    TEST_F(NDBufferTest, NDShapedCreation) {
        auto buff = NDBuffer<int>({32, 32});
        ASSERT_EQ(buff.shape(), NDShape({32, 32}));
    }

    TEST_F(NDBufferTest, TestNO2) {
        ;
        ;
    }

}  // namespace optmath
