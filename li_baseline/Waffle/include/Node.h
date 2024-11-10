#pragma once

#include "common.h"

struct NbEntry {
    Entry entry;
    double dist = numeric_limits<float>::max();
    bool operator<(NbEntry const &second) const { return dist < second.dist; }
};

struct NbNode {
    struct cmp {
        bool operator()(NbNode* const &first, NbNode* const &second) {
            return first->dist > second->dist;
        }
    };

    NbNode *parent = NULL;
    double dist = numeric_limits<float>::max();

    // bool operator>(NbNode const &second) const { return dist > second.dist; }

    virtual void search(const Point&, min_heap<NbNode *, cmp>&, max_heap<NbEntry> &, vector<NbNode *> &) = 0;
    virtual Info track() = 0;
    virtual ~NbNode() = default;
};

struct Node {
    struct Split {
        Point pt;
        bool axis;
    };

    Rect rect = {
        sqrt(numeric_limits<float>::max())/2,
        sqrt(numeric_limits<float>::max())/2,
        -sqrt(numeric_limits<float>::max())/2,
        -sqrt(numeric_limits<float>::max())/2,
    };

    // Rect methods
    bool contains(Point const &) const;
    Point getCenter() const;
    bool inside(Rect const &) const;
    double minSqrDist(Rect const &) const;
    double minSqrDist(Point const &) const;
    bool overlap(Rect const &) const;
    Rect getRect(Point const &) const;
    Rect getRect(Rect const &) const;

    // Node methods
    virtual void aggrInfo(Info&) const = 0;
    virtual uint findHeight() const = 0;
    virtual NbNode* getNbNode() = 0;
    virtual Info insert(Node *, uint, Entry const &) = 0;
    virtual Info range(Rect const &) = 0;
    virtual uint size(About&) const = 0;
    virtual array<Node*, 2> split(Node *, uint) = 0;
    virtual array<Node*, 2> split(Node *) = 0;
    virtual void snapshot(ofstream&) const = 0;
    virtual void unbind(Node *) = 0;

    virtual ~Node() = default;
};

struct Directory : Node {
    static uint capacity;
    Info ledger;
    vector<Node*> contents;
    vector<Split> splits;

    Directory();

    void aggrInfo(Info &) const;
    uint findHeight() const;
    void fusion(Node *);
    NbNode* getNbNode();
    Info insert(Node *pn, uint, Entry const &);
    Info range(Rect const &);
    Info refresh();
    uint size(About&) const;
    array<Node*, 2> split(Node *, uint);
    array<Node*, 2> split(Node *);
    void snapshot(ofstream&) const;
    void unbind(Node *);

    ~Directory();
};

struct NbDirectory : NbNode {
    Directory *self;
    unordered_set<NbNode *> branch;

    explicit NbDirectory(Directory *);

    void enlist(NbNode *);
    void search(Point const &, min_heap<NbNode *, cmp>&, max_heap<NbEntry> &, vector<NbNode *> &);
    Info track();
    ~NbDirectory();
};

struct Page : Node {
    static uint capacity;
    vector<Entry> entries;

    Page();

    void aggrInfo(Info &) const;
    uint findHeight() const;
    void fission(Node *);
    NbNode* getNbNode();
    Info insert(Node *pn, uint, Entry const &);
    Info range(Rect const &);
    uint size(About&) const;
    array<Node*, 2> split(Node *, uint);
    array<Node*, 2> split(Node *);
    void snapshot(ofstream&) const;
    void unbind(Node *);

    ~Page();
};

struct NbPage : NbNode {
    Page *self;

    explicit NbPage(Page *);

    void search(Point const &, min_heap<NbNode *, cmp>&, max_heap<NbEntry> &, vector<NbNode *> &);
    Info track();
    ~NbPage();
};
