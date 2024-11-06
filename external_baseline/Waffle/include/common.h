#pragma once

#include "config.h"

#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <fstream>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <limits>
#include <math.h>
#include <map>
#include <queue>
#include <vector>
#include <sstream>
#include <stack>
#include <string.h>
#include <unordered_set>

using namespace std;
using namespace chrono;

#define TRACE
#ifdef TRACE
#define trace(...) __f(#__VA_ARGS__, __VA_ARGS__)
template <typename Arg1> void __f(const char *name, Arg1 &&arg1) {
    cerr << name << " : " << arg1 << endl;
}
template <typename Arg1, typename... Args>
void __f(const char *names, Arg1 &&arg1, Args &&... args) {
    const char *comma = strchr(names + 1, ',');
    cerr.write(names, comma - names) << " : " << setw(9) << arg1 << " | ";
    __f(comma + 1, args...);
}
#else
#define trace(...)
#endif

#define all(c) c.begin(), c.end()
#define remove(container, element) container.erase(find(all(container), element))

constexpr uint D = 2;
constexpr bool V = 0;
constexpr bool H = 1;
using Rect = array<float, 2*D>;
using Point = array<float, D>;
template<typename T> using max_heap = priority_queue<T, vector<T>>;
// template<typename T> using min_heap = priority_queue<T, vector<T>, greater<T>>;
template<typename T, typename C> using min_heap = priority_queue<T, vector<T>, C>;

constexpr double dist(float x1, float y1, float x2, float y2) {
    return pow(x1 - x2, 2) + pow(y1 - y2, 2);
}
constexpr double distManhattan(float x1, float y1, float x2, float y2) {
    return abs(x1 - x2) + abs(y1 - y2);
}
constexpr uint oppDir(uint d) {return (d + D) % (D * 2);};

struct About {
    uint directories = 0;
    uint pages = 0;
    uint splits = 0;
};

struct Entry {
    int id;
    Point pt;
};

struct Info {
    uint entries = 0;
    uint pages = 0;
    uint reads = 0;
    uint writes = 0;

    Info operator+(Info i) {
        return Info{entries+i.entries, pages+i.pages, reads+i.reads, writes+i.writes};
    }
    void operator+=(Info i) {
        *this = *this + i;
    }
};
