#include "NDShape.h"

namespace optmath {

    std::ostream &operator<<(std::ostream &out, const NDShape &other) {
        auto begin = other.begin();
        auto end = other.end();

        out << '{';

        while (true) {
            out << *begin;
            begin++;
            if (begin == end) {
                break;
            }
            out << ',' << ' ';
        }
        out << '}';

        return out;
    }

}  // namespace optmath
