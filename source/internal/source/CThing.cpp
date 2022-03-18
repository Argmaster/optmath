#include "CThing.h"

namespace shapes {

// Default constructor
Thing::Thing() {}

// Overloaded constructor
Thing::Thing(int x0, int y0, int x1, int y1) {
    this->x0 = x0;
    this->y0 = y0;
    this->x1 = x1;
    this->y1 = y1;
}

// Destructor
Thing::~Thing() {}

// Return the area of the Thing
int Thing::getArea() { return (this->x1 - this->x0) * (this->y1 - this->y0); }

// Get the size of the Thing.
// Put the size in the pointer args
void Thing::getSize(int *width, int *height) {
    (*width) = x1 - x0;
    (*height) = y1 - y0;
}

// Move the Thing by dx dy
void Thing::move(int dx, int dy) {
    this->x0 += dx;
    this->y0 += dy;
    this->x1 += dx;
    this->y1 += dy;
}
}  // namespace shapes
