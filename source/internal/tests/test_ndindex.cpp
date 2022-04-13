#include <gtest/gtest.h>

#include <cstdint>

#include "NDIndex.h"

namespace optmath {

    class NDIndexTest : public ::testing::Test {};

    TEST_F(NDIndexTest, NewNDIndex) {
        auto test_index = optmath::NDIndex({2, 1, 4});
        ASSERT_EQ(test_index[0], 2);
        ASSERT_EQ(test_index[1], 1);
        ASSERT_EQ(test_index[2], 4);
        ASSERT_EQ(test_index.size(), 3);
    }

    TEST_F(NDIndexTest, EqualityCheck) {
        ASSERT_EQ(optmath::NDIndex({32, 32}), optmath::NDIndex({32, 32}));
        ASSERT_FALSE(optmath::NDIndex({32, 32}) ==
                     optmath::NDIndex({32, 32, 32}));
        ASSERT_FALSE(optmath::NDIndex({32, 32}) == optmath::NDIndex({3, 32}));
        ASSERT_FALSE(optmath::NDIndex({32, 32}) == optmath::NDIndex({32, 3}));
    }

    TEST_F(NDIndexTest, InequalityCheck) {
        ASSERT_FALSE(optmath::NDIndex({32, 32}) != optmath::NDIndex({32, 32}));
        ASSERT_NE(optmath::NDIndex({32, 32}), optmath::NDIndex({32, 32, 32}));
        ASSERT_NE(optmath::NDIndex({32, 32}), optmath::NDIndex({3, 32}));
        ASSERT_NE(optmath::NDIndex({32, 32}), optmath::NDIndex({32, 3}));
    }

    TEST_F(NDIndexTest, IteratorValueTest) {
        auto test_index = optmath::NDIndex({2, 1, 4});
        std::vector<int64_t> sample({2, 1, 4});

        auto lhsb = test_index.cbegin();
        auto rhsb = sample.cbegin();
        auto lhse = test_index.cend();
        auto rhse = sample.cend();

        ASSERT_EQ(test_index.size(), sample.size());

        while (lhsb != lhse && rhsb != rhse) {
            auto left = *lhsb;
            auto right = *rhsb;

            ASSERT_EQ(left, right);

            lhsb++;
            rhsb++;
        }
    }

    TEST_F(NDIndexTest, ForEachCompatTest) {
        auto test_index = optmath::NDIndex({2, 1, 4});
        std::vector<int64_t> sample({2, 1, 4});

        ASSERT_EQ(test_index.size(), sample.size());

        auto i = 0;
        for (auto &&item : test_index) {
            ASSERT_EQ(item, sample[i]);
            i++;
        }
    }
}  // namespace optmath