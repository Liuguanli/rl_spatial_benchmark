#pragma once

#include "Node.h"
// #include "common.h"

using namespace std;

struct Waffle {

    Node *root;

    Waffle(int, int);

    void snapshot() const;
    void load(string const &, long const &);
    void bulkload(string const &, long const &);
    Info rangeQuery(Rect const &);
    Info deleteQuery(Entry const &);
    Info insertQuery(Entry const &);
    Info kNNQuery(Point const &, uint const &);
    uint size(About &) const;

    ~Waffle();
};
