#include "Node.h"

uint Page::capacity;

/////////////////////////////////////////////////////////////////////////////////////////
// Functions
/////////////////////////////////////////////////////////////////////////////////////////

inline bool overlaps(Rect r, Point p) {
    for (int i = 0; i < D; i++) {
        if (r[i] > p[i] || p[i] > r[i + D])
            return false;
    }
    return true;
}

/////////////////////////////////////////////////////////////////////////////////////////
// Page Methods
/////////////////////////////////////////////////////////////////////////////////////////

Page::Page() {}

void Page::aggrInfo(Info &info) const { info += Info{.entries = uint(entries.size()), .pages = 1}; }

uint Page::findHeight() const { return 0; }

void Page::fission(Node *parent) {
    long splitRank = entries.size() / 2;
    if (splitRank > capacity)
        splitRank = capacity * floor(ceil(entries.size() / float(capacity)) / 2);
    array<Node *, 2> pages = split(parent, splitRank);
    for (auto pg : pages) {
        Page *page = static_cast<Page *>(pg);
        if (page->entries.size() > capacity) {
            page->fission(parent);
            delete page;
        } else
            static_cast<Directory *>(parent)->contents.emplace_back(pg);
    }
}

NbNode *Page::getNbNode() {
    NbNode *NbNode = new NbPage(this);
    return NbNode;
}

Info Page::insert(Node *pn, uint pos, Entry const &e) {
    entries.emplace_back(e);
    Info info{.entries = 1, .writes = 2};
    if (entries.size() > capacity) {
        array<Node *, 2> pages = split(pn);
        Directory *dpn = static_cast<Directory *>(pn);
        dpn->contents.erase(dpn->contents.begin() + pos);
        delete this;
        for (auto pg : pages)
            dpn->contents.emplace_back(pg);
        info.writes = 3;
        info.pages = 1;
    }
    return info;
}

Info Page::range(Rect const &query) {
    Info info;
    uint numEntries = 0;
    if constexpr (DEBUG) {
        if (inside(query))
            numEntries = entries.size();
        else {
            for (auto e : entries)
                if (overlaps(query, e.pt))
                    numEntries++;
        }
    }
    info = Info{.entries = numEntries, .reads = 1};
    return info;
}

uint Page::size(About &about) const {
    about.pages += 1;
    uint nodeSize = 4 * sizeof(float) + sizeof(uint) + sizeof(void *);
    return nodeSize;
}

array<Node *, 2> Page::split(Node *pn, uint splitRank) {
    bool axis = (rect[2] - rect[0]) < (rect[3] - rect[1]);
    sort(all(entries), [axis](Entry const &l, Entry const &r) { return l.pt[axis] < r.pt[axis]; });
    Split newSplit = Split();
    newSplit.axis = axis;
    newSplit.pt[axis] = entries[splitRank].pt[axis];
    newSplit.pt[!axis] = getCenter()[!axis];

    // cerr << "Create new pages" << endl;
    array<Node *, 2> pages = {new Page(), new Page()};

    // Splitting entries
    static_cast<Page *>(pages[0])->entries =
        vector<Entry>(entries.begin(), entries.begin() + splitRank);
    static_cast<Page *>(pages[1])->entries =
        vector<Entry>(entries.begin() + splitRank, entries.end());

    // cerr << "Make bounding rectangles" << endl;
    for (auto page : pages) {
        for (auto e : static_cast<Page *>(page)->entries)
            page->rect = page->getRect(e.pt);
    }

    static_cast<Directory *>(pn)->splits.emplace_back(newSplit);
    return pages;
}

array<Node *, 2> Page::split(Node *pn) {
    uint splitRank = entries.size() / 2;
    return split(pn, splitRank);
}

void Page::snapshot(ofstream &ofs) const {
    ofs << 0 << "," << entries.size();
    for (auto c : rect)
        ofs << "," << c;
    ofs << endl;
}

void Page::unbind(Node *node) {
    Page *page = static_cast<Page *>(node);
    page->entries.insert(page->entries.end(), all(entries));
}

Page::~Page() { entries.clear(); }

/////////////////////////////////////////////////////////////////////////////////////////
// NbPage Methods
/////////////////////////////////////////////////////////////////////////////////////////

NbPage::NbPage(Page *_self) : self(_self){};

void NbPage::search(Point const &queryPt, min_heap<NbNode *, cmp> &unseenNbs,
    max_heap<NbEntry> &knnEntries, vector<NbNode *> &pool) {
    auto calcSqrDist = [](Point x, Point y) {
        return pow((x[0] - y[0]), 2) + pow((x[1] - y[1]), 2);
    };
    for (auto e : self->entries) {
        double minDist = knnEntries.top().dist;
        double eDist = calcSqrDist(queryPt, e.pt);
        if (eDist < minDist) {
            NbEntry nbEnt;
            nbEnt.entry = e;
            nbEnt.dist = eDist;
            knnEntries.pop();
            knnEntries.push(nbEnt);
        }
    }
    if (parent)
        static_cast<NbDirectory *>(parent)->enlist(this);
}

Info NbPage::track() { return Info{.reads = 1}; }

NbPage::~NbPage(){};
