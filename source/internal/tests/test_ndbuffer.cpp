#include <gtest/gtest.h>

#include "NDBuffer.h"

namespace optmath {

    class NDBufferTest : public ::testing::Test {};

    TEST_F(NDBufferTest, NoNullShapeCreation1D) {
        ASSERT_DEATH(NDBufferInt32({0}),
                     "Assertion .*?std::all_of.*?shape_\\.begin.*?failed.");
    }
    TEST_F(NDBufferTest, NoNullShapeCreation2D) {
        ASSERT_DEATH(NDBufferInt32({0, 0}),
                     "Assertion .*?std::all_of.*?shape_\\.begin.*?failed.");
    }
    TEST_F(NDBufferTest, CreationShape1D) {
        auto buff = NDBufferInt32({5389});
        ASSERT_EQ(buff.shape(), NDShape({5389}));
    }
    TEST_F(NDBufferTest, CreationShape2D_I32) {
        auto buff = NDBufferInt32({32, 399});
        ASSERT_EQ(buff.shape(), NDShape({32, 399}));
    }
    TEST_F(NDBufferTest, CreationShape3D_F32) {
        auto buff = NDBufferFloat32({88, 94, 14});
        ASSERT_EQ(buff.shape(), NDShape({88, 94, 14}));
    }
    TEST_F(NDBufferTest, CreationShape4D_F64) {
        auto buff = NDBufferFloat64({88, 94, 14, 43});
        ASSERT_EQ(buff.shape(), NDShape({88, 94, 14, 43}));
    }
    TEST_F(NDBufferTest, CreationShape5D_I64) {
        auto buff = NDBufferInt64({5, 8, 14, 6, 4});
        ASSERT_EQ(buff.shape(), NDShape({5, 8, 14, 6, 4}));
    }
    TEST_F(NDBufferTest, CopyConstruction) {
        auto buff0 = NDBufferInt32({91, 324, 44});

        ASSERT_EQ(buff0.shape(), NDShape({91, 324, 44}));

        auto j = 0;
        for (auto& i : buff0) {
            i = j;
            j++;
        }

        auto buff1 = buff0;

        ASSERT_EQ(buff0.shape(), NDShape({91, 324, 44}));
        ASSERT_EQ(buff1.shape(), NDShape({91, 324, 44}));

        j = 0;
        for (auto& i : buff1) {
            ASSERT_EQ(j, i);
            j++;
        }
    }
    TEST_F(NDBufferTest, CopyAssignment) {
        auto buff0 = NDBufferInt32({32, 432});
        auto buff1 = NDBufferInt32({5, 8});

        ASSERT_EQ(buff1.shape(), NDShape({5, 8}));

        auto j = 0;
        for (auto& i : buff0) {
            i = j;
            j++;
        }

        buff1 = buff0;

        ASSERT_EQ(buff0.shape(), NDShape({32, 432}));
        ASSERT_EQ(buff1.shape(), NDShape({32, 432}));

        j = 0;
        for (auto& i : buff1) {
            ASSERT_EQ(j, i);
            j++;
        }
    }
    TEST_F(NDBufferTest, MoveConstruction) {
        auto buff0 = NDBufferInt32({32, 22});

        auto j = 0;
        for (auto& i : buff0) {
            i = j;
            j++;
        }

        auto buff1(std::move(buff0));

        ASSERT_EQ(buff0.shape(), NDShape({}));
        ASSERT_EQ(buff1.shape(), NDShape({32, 22}));

        j = 0;
        for (auto& i : buff1) {
            ASSERT_EQ(j, i);
            j++;
        }
    }
    TEST_F(NDBufferTest, MoveAssignment) {
        auto buff0 = NDBufferInt32({32, 756, 43});

        auto j = 0;
        for (auto& i : buff0) {
            i = j;
            j++;
        }

        auto buff1 = std::move(buff0);

        ASSERT_EQ(buff0.shape().size(), 0);
        ASSERT_EQ(buff1.shape(), NDShape({32, 756, 43}));

        j = 0;
        for (auto& i : buff1) {
            ASSERT_EQ(j, i);
            j++;
        }
    }
    TEST_F(NDBufferTest, FillWithOneValue) {

        auto sh1 = 43;
        auto sh2 = 156;

        auto buff = NDBufferFloat32({sh1, sh2});

        buff.fill(546.0);

        for (long long i = 0; i < sh1; i++) {
            for (long long j = 0; j < sh2; j++) {
                auto item_1 = buff[{i, j}];
                ASSERT_EQ(item_1, 546.0);
            }
        }
    }
    TEST_F(NDBufferTest, ReshapeVector2Dto1D) {
        auto buff = NDBufferInt32({16, 4});
        buff.fill(0);
        buff.reshape({64});

        ASSERT_EQ(buff.shape(), NDShape({64}));

        for (long long i = 0; i < 64; i++) {
            auto item = buff[{i}];
            ASSERT_EQ(item, 0);
        }
    }
    TEST_F(NDBufferTest, ReshapeVector1Dto2D) {
        auto buff = NDBufferInt32({64});
        buff.fill(0);
        buff.reshape({16, 4});

        ASSERT_EQ(buff.shape(), NDShape({16, 4}));

        for (long long i = 0; i < 16; i++) {
            for (long long j = 0; j < 4; j++) {
                auto item = buff[{i, j}];
                ASSERT_EQ(item, 0);
            }
        }
    }
    TEST_F(NDBufferTest, ElementAccessIncrementHeatmap3D) {
        auto sh1 = 5;
        auto sh2 = 3;
        auto sh3 = 4;

        auto buffer = NDBufferInt64({sh1, sh2, sh3});
        buffer.fill(0LL);

        for (index_t i = 0; i < sh1; i++) {
            for (index_t j = 0; j < sh2; j++) {
                for (index_t k = 0; k < sh3; k++) {
                    auto index = NDIndex({i, j, k});
                    buffer[index]++;
                }
            }
        }

        for (index_t i = 0; i < sh1; i++) {
            for (index_t j = 0; j < sh2; j++) {
                for (index_t k = 0; k < sh3; k++) {
                    auto test_val = buffer[{i, j, k}];
                    ASSERT_EQ(test_val, 1);
                }
            }
        }
    }
    TEST_F(NDBufferTest, ElementAccessIncrementHeatmap4D) {
        auto sh1 = 16;
        auto sh2 = 9;
        auto sh3 = 7;
        auto sh4 = 6;

        auto buffer = NDBufferInt64({sh1, sh2, sh3, sh4});

        ASSERT_EQ(buffer.buffer_size(), 6048);
        buffer.fill(0LL);

        index_t iter_c = 0;

        for (index_t i = 0; i < sh1; i++) {
            for (index_t j = 0; j < sh2; j++) {
                for (index_t k = 0; k < sh3; k++) {
                    for (index_t g = 0; g < sh4; g++) {
                        auto index = NDIndex({i, j, k, g});

                        ASSERT_EQ(buffer.shape().in_buffer_position(index),
                                  iter_c);
                        ASSERT_LT(iter_c, 6048);

                        buffer[index]++;
                        iter_c++;
                    }
                }
            }
        }
        iter_c = 0;
        for (index_t i = 0; i < sh1; i++) {
            for (index_t j = 0; j < sh2; j++) {
                for (index_t k = 0; k < sh3; k++) {
                    for (index_t g = 0; g < sh4; g++) {
                        auto index = NDIndex({i, j, k, g});

                        ASSERT_EQ(buffer.shape().in_buffer_position(index),
                                  iter_c);
                        ASSERT_LT(iter_c, 6048);

                        std::cout << index << " "
                                  << buffer.shape().in_buffer_position(index)
                                  << std::endl;

                        auto test_val = buffer[index];
                        ASSERT_EQ(test_val, 1);
                        iter_c++;
                    }
                }
            }
        }
    }
    TEST_F(NDBufferTest, ExtendedElementAccess) {
        auto buffer = NDBufferInt64({4, 3, 5});

        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    buffer[{i, j, k}] = i + j + k;
                }
            }
        }

        for (index_t i = 0; i < 4; i++) {
            for (index_t j = 0; j < 3; j++) {
                for (index_t k = 0; k < 5; k++) {
                    auto test_val = buffer[{i, j, k}];
                    std::cout << test_val << " " << i + j + k << std::endl;
                    ASSERT_EQ(test_val, i + j + k);
                }
            }
        }
    }
    TEST_F(NDBufferTest, CommonIterateBuffer) {
        auto buff = NDBufferInt32({2, 2});

        buff[{0, 0}] = 0;
        buff[{0, 1}] = 1;
        buff[{1, 0}] = 2;
        buff[{1, 1}] = 3;

        auto j = 0;

        for (auto&& i : buff) {
            ASSERT_EQ(i, j);
            j++;
        }
    }
    TEST_F(NDBufferTest, IterateAndSetValues) {
        auto buff = NDBufferInt32({2, 2});

        for (auto& i : buff) {
            i = 932;
        }

        for (auto i : buff) {
            ASSERT_EQ(i, 932);
        }
    }
    TEST_F(NDBufferTest, BufferEqualityOp) {
        auto first  = NDBufferInt32({2, 2});
        auto second = NDBufferInt32({2, 2});

        auto j = 0;
        for (auto& i : first) {
            i = j;
            j++;
        }

        j = 0;
        for (auto& i : second) {
            i = j;
            j++;
        }

        ASSERT_EQ(first, second);
    }
    TEST_F(NDBufferTest, Stringify) {
        auto first = NDBufferInt32({3, 2});

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
} // namespace optmath
