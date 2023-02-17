#pragma once
#include <iostream>

using namespace std;

namespace algorithm {
    void fast_sort();
    inline void main() {
        cout << "------- algorithm ------" << endl;
        fast_sort();
        cout << "======= algorithm end =======" << endl;
    }
};