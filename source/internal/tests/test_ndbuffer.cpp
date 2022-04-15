#include <gtest/gtest.h>

#include "NDBuffer.h"

namespace optmath {

    class NDBufferTest : public ::testing::Test {};

    TEST_F(NDBufferTest, NDShapedCreation) {
        auto buff = NDBuffer<int>({32, 32});

        ASSERT_EQ(buff.shape(), NDShape({32, 32}));
    }

    TEST_F(NDBufferTest, FillWithOneValue) {
        auto buff = NDBuffer<int>({32, 32});

        buff.fill(33);

        for (long long i = 0; i < 32; i++) {
            for (long long j = 0; j < 32; j++) {
                auto item_1 = buff[{i, j}];
                ASSERT_EQ(item_1, 33);
            }
        }
    }

    TEST_F(NDBufferTest, ReshapeVector) {
        auto buff = NDBuffer<int>({32, 32});
        buff.fill(0);
        buff.reshape({1024});

        ASSERT_EQ(buff.shape(), NDShape({1024}));

        for (long long i = 0; i < 1024; i++) {
            auto item_1 = buff[{i}];
            ASSERT_EQ(item_1, 0);
        }
    }

    TEST_F(NDBufferTest, BufferReferences) {
        auto buff = NDBuffer<int>({32, 32});
        ASSERT_EQ(buff.buffer_reference_count(), 1);
        // auto buff2 = buff;
    }

}  // namespace optmath
