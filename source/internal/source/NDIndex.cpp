#include "NDIndex.h"

namespace optmath {

    bool operator==(const NDIndex &lhs, const NDIndex &rhs) {
        if (lhs.size() == rhs.size()) {
            auto lhsb = lhs.cbegin();
            auto rhsb = rhs.cbegin();
            auto lhse = lhs.cend();
            auto rhse = rhs.cend();

            while (lhsb != lhse && rhsb != rhse) {
                auto left = *lhsb;
                auto right = *rhsb;
                if (left != right) return false;
                lhsb++;
                rhsb++;
            }
            return true;
        }
        return false;
    }

    bool operator!=(const NDIndex &lhs, const NDIndex &rhs) {
        return !(lhs == rhs);
    }

}  // namespace optmath
