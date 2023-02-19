#pragma once
#include <iostream>

using namespace std;

namespace chapter1 {
    void stage1();
    inline void main() {
        cout << "----- Chapter1 -----" << endl;
        stage1();
        cout << "----- Chapter1 end -----" << endl;
    }
};