#include "Waffle.h"

void printRect(string msg, Rect r) {
    cerr << msg << ": " << r[0] << " | " << r[1] << " | " << r[2] << " | " << r[3] << endl;
}

Waffle::Waffle(int _directoryCap, int _pageCap) {
    Directory::capacity = _directoryCap;
    Page::capacity = _pageCap;
    root = new Directory();
    Directory *dRoot = static_cast<Directory *>(root);
    dRoot->ledger = Info{.pages = 1};

    Node *firstPage = new Page();
    dRoot->contents.emplace_back(firstPage);
}

void Waffle::bulkload(string const &filename, long const &limit) {
    string line;
    ifstream file(filename);

    int i = 0;
    Directory *dRoot = static_cast<Directory *>(root);
    Page *firstPage = static_cast<Page *>(dRoot->contents.front());
    firstPage->entries.reserve(limit);
    if (file.is_open()) {
        // getline(file, line);
        while (getline(file, line)) {
            int id;
            float lat, lon;
            istringstream buf(line);
            buf >> id >> lon >> lat;
            Entry e;
            e.id = id;
            e.pt = {lon, lat};
            firstPage->entries.emplace_back(e);
            root->rect = root->getRect(e.pt);
            firstPage->rect = root->getRect(e.pt);
            if (++i >= limit)
                break;
        }
        file.close();
    } else
        cerr << "Data file " << filename << " not found!";

    cout << "Initiate page fission" << endl;
    // Clear root of any existing contents.
    dRoot->contents.clear();
    dRoot->ledger.pages = ceil(firstPage->entries.size() / Page::capacity);
    dRoot->ledger.entries = firstPage->entries.size();
    firstPage->fission(root);
    delete firstPage;

    cout << "Initiate directory fission" << endl;
    while (dRoot->contents.size() > Directory::capacity)
        dRoot->fusion(root);
}

Info Waffle::deleteQuery(Entry const &p) {
    /* Node *node = root;
    while (node->contents) {
        auto cn = node->contents->begin();
        while (!(*cn)->containsPt(p.data))
            cn++;
        node = *cn;
    } */
    Info stats;
    return stats;
}

Info Waffle::insertQuery(Entry const &e) {
    if (!root->contains(e.pt))
        root->rect = root->getRect(e.pt);
    Info info = root->insert(root, 0, e);
    return info;
}

Info Waffle::kNNQuery(Point const &queryPt, uint const &k) {
    min_heap<NbNode *, NbNode::cmp> unseenNbs;
    vector<NbEntry> tempEntries(k);
    max_heap<NbEntry> knnEntries(all(tempEntries));
    vector<NbNode *> pool;
    NbNode *rootNb = root->getNbNode();
    rootNb->dist = root->minSqrDist(queryPt);
    unseenNbs.emplace(rootNb);
    pool.emplace_back(rootNb);

    while (!unseenNbs.empty()) {
        NbNode *nb = unseenNbs.top();
        unseenNbs.pop();
        double minDist = knnEntries.top().dist;
        if (nb->dist < minDist)
            nb->search(queryPt, unseenNbs, knnEntries, pool);
        else
            break;
    }

    if constexpr (DEBUG) {
        if (k == 32) {
            while (!knnEntries.empty()) {
                Entry entry = knnEntries.top().entry;
                double sqrDist = knnEntries.top().dist;
                knnEntries.pop();
                trace(entry.id, sqrDist);
            }
            cerr << endl;
        }
    }

    Info info = rootNb->track();
    for (auto kn : pool)
        delete kn;
    return info;
}

Info Waffle::rangeQuery(Rect const &query) {
    Info info = root->range(query);
    if constexpr (DEBUG) {
        int numEntries = info.entries;
        trace(numEntries);
        cerr << endl;
    }
    return info;
}

void Waffle::snapshot() const {
    ofstream ofs("Index.csv");
    root->snapshot(ofs);
    ofs.close();
}

uint Waffle::size(About &about) const { return root->size(about); }

Waffle::~Waffle() { delete root; }
