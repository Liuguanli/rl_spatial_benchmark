#include "Node.h"

uint Directory::capacity;

/////////////////////////////////////////////////////////////////////////////////////////
// Directory Methods
/////////////////////////////////////////////////////////////////////////////////////////

Directory::Directory() {}

void Directory::aggrInfo(Info &info) const {
    for (auto node : contents)
        node->aggrInfo(info);
}

uint Directory::findHeight() const { return contents.front()->findHeight() + 1; }

void Directory::fusion(Node *parent) {
    array<Node *, 2> dirs = split(parent);
    for (auto nd : dirs) {
        Directory *dir = static_cast<Directory *>(nd);
        if (dir->contents.size() > capacity) {
            dir->fusion(parent);
            delete dir;
        } else
            static_cast<Directory *>(parent)->contents.emplace_back(dir);
    }
}

NbNode *Directory::getNbNode() {
    NbNode *nb = new NbDirectory(this);
    return nb;
}

Info Directory::insert(Node *parent, uint pos, Entry const &e) {
    Info info;
    int key = -1;

    // Check if a child node contains the entry.
    for (uint i = 0; i < contents.size(); i++) {
        if (contents[i]->contains(e.pt)) {
            key = i;
            break;
        }
    }
    // If no child node contains the entry, find one to expand
    if (key < 0) {
        Rect container = rect;
        for (auto s : splits) {
            bool lCheck = container[0] < s.pt[0];
            bool rCheck = container[2] > s.pt[0];
            bool dCheck = container[1] < s.pt[1];
            bool uCheck = container[3] > s.pt[1];
            if (lCheck && rCheck && dCheck && uCheck) {
                if (e.pt[s.axis] > s.pt[s.axis]) {
                    container[s.axis] = max(container[s.axis], s.pt[s.axis]);
                } else {
                    container[s.axis + D] = min(container[s.axis + D], s.pt[s.axis]);
                }
            }
        }
        for (uint i = 0; i < contents.size(); i++) {
            Node *cn = contents[i];
            if (cn->inside(container)) {
                key = i;
                cn->rect = cn->getRect(e.pt);
                break;
            }
        }
    }
    Node *cn = contents[key];

    info = cn->insert(this, key, e);
    ledger.pages += info.pages;
    ledger.entries++;
    ledger.writes += info.writes;
    if (contents.size() > capacity) {
        array<Node *, 2> dirs = split(parent);
        Directory *parentDir = static_cast<Directory *>(parent);
        if (this == parent) // if root.
            parentDir->contents.clear();
        else {
            parentDir->contents.erase(parentDir->contents.begin() + pos);
            delete this;
        }
        for (auto dir : dirs)
            parentDir->contents.emplace_back(dir);
    }
    return info;
}

Info Directory::range(Rect const &query) {
    Info info;
    for (auto cn : contents) {
        if (cn->overlap(query))
            info += cn->range(query);
    }
    ledger.pages += info.pages;
    ledger.reads += info.reads;
    info += refresh();
    return info;
}

Info Directory::refresh() {
    if (ledger.entries && findHeight() == 1) { // Limit refreshing to height 1.
        float fat = (ledger.pages / ceil(ledger.entries / float(Page::capacity))) - 1;
        float tolerance = float(ledger.writes) / ledger.reads;
        if (fat > tolerance) {
            int numPages = ledger.pages;
            Node *dummy = new Page();
            dummy->rect = rect;
            unbind(dummy);
            contents.clear();
            splits.clear();
            static_cast<Page *>(dummy)->fission(this);
            delete dummy;
            ledger.pages = contents.size();
            ledger.writes += numPages + ledger.pages;
            return Info{.pages = ledger.pages - numPages, .writes = numPages + ledger.pages};
        }
    }
    return Info();
}

uint Directory::size(About &about) const {
    about.directories += 1;
    about.splits += splits.size();
    uint totalSize = 0;
    for (auto cn : contents)
        totalSize += cn->size(about);
    totalSize += 4 * sizeof(float) + sizeof(uint) + sizeof(void *);  // Node size
    totalSize += splits.size() * (2 * sizeof(float) + sizeof(bool)); // Split sizes
    totalSize += 4 * sizeof(uint);                                   // ledger size
    return totalSize;
}

array<Node *, 2> Directory::split(Node *pn) {
    array<Node *, 2> dirs = {new Directory(), new Directory()};
    Split bestSplit = splits[0];

    // cerr << "Make bounding rectangles" << endl;
    for (auto cn : contents) {
        bool side = cn->getCenter()[bestSplit.axis] > bestSplit.pt[bestSplit.axis];
        static_cast<Directory *>(dirs[side])->contents.emplace_back(cn);
        dirs[side]->rect = dirs[side]->getRect(cn->rect);
    }

    // cerr << "Distribute splits" << endl;
    for (auto isplit = next(splits.begin()); isplit != splits.end(); isplit++) {
        bool side = (*isplit).pt[bestSplit.axis] > bestSplit.pt[bestSplit.axis];
        static_cast<Directory *>(dirs[side])->splits.emplace_back(*isplit);
    }

    for (auto node : dirs) {
        Directory *dir = static_cast<Directory *>(node);
        dir->aggrInfo(dir->ledger);
        dir->ledger += Info{.reads = (ledger.reads + 1) / 2, .writes = (ledger.writes + 1) / 2};
    }

    contents.clear();
    splits.clear();
    static_cast<Directory *>(pn)->splits.emplace_back(bestSplit);
    return dirs;
}

array<Node *, 2> Directory::split(Node *pn, uint splitRank) { return split(pn); }

void Directory::snapshot(ofstream &ofs) const {
    ofs << findHeight() << "," << contents.size();
    for (auto c : rect)
        ofs << "," << c;
    ofs << endl;
    for (auto cn : contents)
        cn->snapshot(ofs);
}

void Directory::unbind(Node *node) {
    for (auto cn : contents) {
        cn->unbind(node);
        delete cn;
    }
    contents.clear(); // To prevent double deletion.
}

Directory::~Directory() {
    for (auto cn : contents)
        delete cn;
    contents.clear();
    splits.clear();
}

/////////////////////////////////////////////////////////////////////////////////////////
// NbDirectory Methods
/////////////////////////////////////////////////////////////////////////////////////////

NbDirectory::NbDirectory(Directory *_self) : self(_self){};

void NbDirectory::enlist(NbNode *childNb) {
    branch.emplace(childNb);
    if (parent)
        static_cast<NbDirectory *>(parent)->enlist(this);
}

void NbDirectory::search(Point const &queryPt, min_heap<NbNode *, cmp> &unseenNbs,
    max_heap<NbEntry> &knnEntries, vector<NbNode *> &pool) {
    double minDist = knnEntries.top().dist;
    for (auto cn : self->contents) {
        double cnDist = cn->minSqrDist(queryPt);
        if (cnDist < minDist) {
            NbNode *childNb = cn->getNbNode();
            childNb->parent = this;
            childNb->dist = cnDist;
            unseenNbs.emplace(childNb);
            pool.emplace_back(childNb);
        }
    }
}

Info NbDirectory::track() {
    Info info;
    for (auto nb : branch)
        info += nb->track();
    self->ledger.pages += info.pages;
    self->ledger.reads += info.reads;
    info += self->refresh();
    return info;
}

NbDirectory::~NbDirectory() { branch.clear(); };
