#ifndef Thing_H
#define Thing_H
#include <iostream>

namespace shapes {
    class Thing {
      public:
        int x0, y0, x1, y1;
        Thing();
        Thing(int x0, int y0, int x1, int y1);
        ~Thing();
        int  getArea();
        void getSize(int* width, int* height);
        void move(int dx, int dy);
    };
} // namespace shapes

#endif
