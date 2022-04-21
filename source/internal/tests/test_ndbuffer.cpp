#include <gtest/gtest.h>

#include "NDBuffer.h"

namespace optmath {

    class NDBufferTest : public ::testing::Test {};

    TEST_F(NDBufferTest, FromNDShapedCreation) {
        auto buff = NDBuffer<int>({32, 32});
        ASSERT_EQ(buff.shape(), NDShape({32, 32}));
    }

    TEST_F(NDBufferTest, CopyConstruction) {
        auto buff0 = NDBuffer<int>({32, 32});
        auto buff1 = buff0;
        ASSERT_EQ(buff0.buffer_reference_count(), 2);
        ASSERT_EQ(buff1.buffer_reference_count(), 2);
        ASSERT_EQ(buff0.shape(), NDShape({32, 32}));
        ASSERT_EQ(buff1.shape(), NDShape({32, 32}));
    }

    TEST_F(NDBufferTest, CopyAssignment) {
        auto buff0 = NDBuffer<int>({32, 32});
        auto buff1 = NDBuffer<int>({5, 5});
        ASSERT_EQ(buff1.shape(), NDShape({5, 5}));
        buff0 = buff1;
        ASSERT_EQ(buff0.buffer_reference_count(), 2);
        ASSERT_EQ(buff1.buffer_reference_count(), 2);
        ASSERT_EQ(buff0.shape(), NDShape({5, 5}));
        ASSERT_EQ(buff1.shape(), NDShape({5, 5}));
    }

    TEST_F(NDBufferTest, MoveConstruction) {
        auto buff0 = NDBuffer<int>({32, 32});
        auto buff1(std::move(buff0));
        ASSERT_EQ(buff0.buffer_reference_count(), 0);
        ASSERT_EQ(buff1.buffer_reference_count(), 1);
        ASSERT_EQ(buff0.shape(), NDShape({}));
        ASSERT_EQ(buff1.shape(), NDShape({32, 32}));
    }

    TEST_F(NDBufferTest, MoveAssignment) {
        auto buff0 = NDBuffer<int>({32, 32});
        auto buff1 = std::move(buff0);
        ASSERT_EQ(buff0.buffer_reference_count(), 0);
        ASSERT_EQ(buff1.buffer_reference_count(), 1);
        ASSERT_EQ(buff0.shape().size(), 0);
        ASSERT_EQ(buff1.shape(), NDShape({32, 32}));
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

    TEST_F(NDBufferTest, AccessInNDimensions) {
        auto buff = NDBuffer<int>({5, 5, 6, 2});
        buff.fill(0);
        auto value = buff[{1, 3, 2, 0}];
        ASSERT_EQ(value, 0);
    }

    TEST_F(NDBufferTest, WriteSingleValue) {
        auto buff = NDBuffer<int>({5, 5, 6, 2});

        auto value = buff[{1, 3, 2, 0}];
        value      = 333;
        ASSERT_EQ(value, 333);
    }

    TEST_F(NDBufferTest, BufferReferencesOnRebind) {
        auto buff = NDBuffer<int>({32, 32});
        ASSERT_EQ(buff.buffer_reference_count(), 1);
        auto buff2 = NDBuffer<int>({32, 32});
        buff2.rebind(buff);
        ASSERT_EQ(buff.buffer_reference_count(), 2);
        ASSERT_EQ(buff2.buffer_reference_count(), 2);
    }

} // namespace optmath
