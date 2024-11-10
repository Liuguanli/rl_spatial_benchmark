#include "Waffle.h"

struct Stats {
    struct StatType {
        long count = 0;
        long io = 0;
    };

    StatType del;
    StatType insert;
    map<int, StatType> knn;
    map<float, StatType> range;
    StatType reload;
};

void knnQuery(tuple<char, vector<float>, float> q, Waffle *index, Stats &stats) {
    Point p;
    for (uint i = 0; i < p.size(); i++)
        p[i] = get<1>(q)[i];
    uint k = get<2>(q);
    Info info = index->kNNQuery(p, k);
    stats.knn[k].io += info.reads;
    if (info.writes > 0) {
        stats.reload.count++;
        stats.reload.io += info.writes;
    }
    stats.knn[k].count++;
}

void rangeQuery(tuple<char, vector<float>, float> q, Waffle *index, Stats &stats) {
    Rect query;
    for (uint i = 0; i < query.size(); i++)
        query[i] = get<1>(q)[i];
    float rs = get<2>(q);

    Info info = index->rangeQuery(query);
    stats.range[rs].io += info.reads;
    if (info.writes > 0) {
        stats.reload.count++;
        stats.reload.io += info.writes;
    }
    stats.range[rs].count++;
}

void insertQuery(tuple<char, vector<float>, float> q, Waffle *index, Stats &stats) {
    Entry p;
    for (uint i = 0; i < p.pt.size(); i++)
        p.pt[i] = get<1>(q)[i];
    p.id = get<2>(q);
    Info info = index->insertQuery(p);
    stats.insert.io += info.writes;
    stats.insert.count++;
}

void deleteQuery(tuple<char, vector<float>, float> q, Waffle *index, Stats &stats) {
    Entry p;
    for (uint i = 0; i < p.pt.size(); i++)
        p.pt[i] = get<1>(q)[i];
    p.id = get<2>(q);
    index->deleteQuery(p);
    stats.del.count++;
}

void evaluate(Waffle *index, string opFile, string logFile) {
    Stats stats;
    auto roundit = [](float val, int d = 2) { return round(val * pow(10, d)) / pow(10, d); };

    cout << "Begin Querying " << opFile << endl;
    string line;
    ifstream file(opFile);
    if (file.is_open()) {
        // getline(file, line); // Skip the header line
        while (getline(file, line)) {
            char type = line[line.find_first_not_of(" ")];
            tuple<char, vector<float>, float> q;
            vector<float> pts;
            if (type == 'l') {
                q = make_tuple(type, pts, 0);
            } else {
                line = line.substr(line.find_first_of(type) + 1);
                const char *cs = line.c_str();
                char *end;
                int params = (type == 'r') ? 4 : 2;
                for (uint d = 0; d < params; d++) {
                    pts.emplace_back(strtof(cs, &end));
                    cs = end;
                }
                float info = strtof(cs, &end);
                q = make_tuple(type, pts, info);
            }
            if (get<0>(q) == 'k') {
                knnQuery(q, index, stats);
            } else if (get<0>(q) == 'r') {
                rangeQuery(q, index, stats);
            } else if (get<0>(q) == 'i') {
                insertQuery(q, index, stats);
            } else if (get<0>(q) == 'd') {
                deleteQuery(q, index, stats);
            } else if (get<0>(q) == 'z') {
                stats = Stats();
            } else if (get<0>(q) == 'l') {
                ofstream log;
                log.open(logFile, ios_base::app);
                if (!log.is_open())
                    cerr << "Unable to open log.txt";

                log << "------------------Results-------------------" << endl << endl;

                log << "------------------Range Queries-------------------" << endl;
                log << setw(8) << "Size" << setw(8) << "Count" << setw(8) << "I/O" << setw(8)
                    << endl;
                for (auto &l : stats.range) {
                    log << setw(8) << l.first << setw(8) << l.second.count << setw(8)
                        << roundit(l.second.io / double(l.second.count)) << endl;
                }

                log << endl << "------------------KNN Queries-------------------" << endl;
                log << setw(8) << "k" << setw(8) << "Count" << setw(8) << "I/O" << setw(8) << endl;
                for (auto &l : stats.knn) {
                    log << setw(8) << l.first << setw(8) << l.second.count << setw(8)
                        << roundit(l.second.io / double(l.second.count)) << endl;
                }

                log << endl << "------------------Insert Queries-------------------" << endl;
                log << "Count:\t" << stats.insert.count << endl;
                log << "I/O:\t" << stats.insert.io / double(stats.insert.count) << endl;

                log << endl << "------------------ Reloading -------------------" << endl;
                log << "Count:\t" << stats.reload.count << endl;
                log << "I/O (overall):\t" << stats.reload.io << endl << endl;

                About about;
                float indexSize = index->size(about);
                log << "Waffle size in MB: " << float(indexSize / 1e6) << endl;
                log << "No. of directories: " << about.directories << endl;
                log << "No. of pages: " << about.pages << endl;
                log << "No. of splits: " << about.splits << endl;

                log << endl << "************************************************" << endl;

                log.close();
            } else
                cerr << "Invalid Query!!!" << endl;
        }
        file.close();
    }
    cout << "Finish Querying..." << endl;
}

int main(int argCount, char **args) {
    string dataFile, opFile;
    if constexpr (BULKLOAD) {
        if (argCount != 3) {
            cerr << "Error: Incorrect usage, please refer to the README" << endl;
            return 0;
        }
        dataFile = string(args[1]);
        opFile = string(args[2]);
    } else {
        if (argCount != 2) {
            cerr << "Error: Incorrect usage, please refer to the README" << endl;
            return 0;
        }
        opFile = string(args[1]);
    }

    string logFile = "log.txt";
    ofstream log(logFile);
    if (!log.is_open())
        cout << "Unable to open log.txt";
    cout << "Defining Waffle..." << endl;
    Waffle index = Waffle(FANOUT, PAGECAP);
    if constexpr (BULKLOAD) {
        cout << "Bulkloading Waffle..." << endl;
        index.bulkload(dataFile, BLL);
    }
    log << "Directory Capacity: " << FANOUT << endl;
    log << "Page Capacity: " << PAGECAP << endl;

    if constexpr (EVAL) {
        cout << "---Evaluation--- " << endl;
        evaluate(&index, opFile, logFile);
    }
    if constexpr (SNAPSHOT)
        index.snapshot();
    return 0;
}
