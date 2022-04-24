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
    TEST_F(NDIndexTest, CopyConstruction) {
        auto test_index = optmath::NDIndex({2, 1, 4});
        { auto test_index_copy{test_index}; }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }
    TEST_F(NDIndexTest, CopyAssignment) {
        auto test_index = optmath::NDIndex({2, 1, 4});
        {
            optmath::NDIndex test_index_copy{3, 3};
            ASSERT_EQ(test_index_copy[0], 3);
            ASSERT_EQ(test_index_copy[1], 3LL);
            test_index_copy = test_index;
            ASSERT_EQ(test_index_copy[0], 2LL);
            ASSERT_EQ(test_index_copy[1], 1LL);
            ASSERT_EQ(test_index_copy[2], 4LL);
        }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }
    TEST_F(NDIndexTest, MoveConstruction) {
        auto test_index_copy{std::move(optmath::NDIndex({2, 1, 4}))};
        ASSERT_EQ(test_index_copy[0], 2LL);
        ASSERT_EQ(test_index_copy[1], 1LL);
        ASSERT_EQ(test_index_copy[2], 4LL);
    }
    TEST_F(NDIndexTest, MoveAssignment) {
        optmath::NDIndex test_index_copy{3, 3};
        ASSERT_EQ(test_index_copy[0], 3);
        ASSERT_EQ(test_index_copy[1], 3LL);
        test_index_copy = optmath::NDIndex({2, 1, 4});
        ASSERT_EQ(test_index_copy[0], 2LL);
        ASSERT_EQ(test_index_copy[1], 1LL);
        ASSERT_EQ(test_index_copy[2], 4LL);
    }
    TEST_F(NDIndexTest, EqualityCheck1DSameSize) {
        ASSERT_EQ(optmath::NDIndex({3}), optmath::NDIndex({3}));
        ASSERT_EQ(optmath::NDIndex({4333}), optmath::NDIndex({4333}));
        ASSERT_EQ(optmath::NDIndex({0}), optmath::NDIndex({0}));

        ASSERT_NE(optmath::NDIndex({243335}), optmath::NDIndex({4355445}));
        ASSERT_NE(optmath::NDIndex({432}), optmath::NDIndex({234}));
    }
    TEST_F(NDIndexTest, EqualityCheck2DSameSize) {
        ASSERT_EQ(optmath::NDIndex({3, 4}), optmath::NDIndex({3, 4}));
        ASSERT_EQ(optmath::NDIndex({4333, 234}),
                  optmath::NDIndex({4333, 234}));
        ASSERT_EQ(optmath::NDIndex({0, 0}), optmath::NDIndex({0, 0}));

        ASSERT_NE(optmath::NDIndex({243335, 1}),
                  optmath::NDIndex({4355445, 1}));
        ASSERT_NE(optmath::NDIndex({432, 43}), optmath::NDIndex({432, 55}));
    }
    TEST_F(NDIndexTest, EqualityCheck3DDiffrentSize) {
        ASSERT_NE(optmath::NDIndex({1, 32}), optmath::NDIndex({1, 32, 0}));
        ASSERT_NE(optmath::NDIndex({1, 4, 23, 5, 12}),
                  optmath::NDIndex({1, 4, 57, 32, 12, 44}));

        ASSERT_NE(optmath::NDIndex({44, 34}), optmath::NDIndex({44, 34, 1}));
    }
    TEST_F(NDIndexTest, IteratorValueTest) {
        auto test_index = optmath::NDIndex({43, 23, 12, 54, 0, 32, 3466});
        std::vector<int64_t> sample({43, 23, 12, 54, 0, 32, 3466});

        auto lhsb = test_index.cbegin();
        auto rhsb = sample.cbegin();
        auto lhse = test_index.cend();
        auto rhse = sample.cend();

        ASSERT_EQ(test_index.size(), sample.size());

        while (lhsb != lhse && rhsb != rhse) {
            auto left  = *lhsb;
            auto right = *rhsb;

            ASSERT_EQ(left, right);

            lhsb++;
            rhsb++;
        }
    }
    TEST_F(NDIndexTest, ForEachCompatTest) {
        auto                 test_index = optmath::NDIndex({2, 1, 4});
        std::vector<int64_t> sample({2, 1, 4});

        ASSERT_EQ(test_index.size(), sample.size());

        auto i = 0;
        for (auto&& item : test_index) {
            ASSERT_EQ(item, sample[i]);
            i++;
        }
    }
    TEST_F(NDIndexTest, ForEachAccessNoRepeat) {
        auto test_index = optmath::NDIndex({0, 1, 2, 3, 4});
        auto i          = 0;
        for (auto&& item : test_index) {
            ASSERT_EQ(item, i);
            i++;
        }
    }
} // namespace optmath
