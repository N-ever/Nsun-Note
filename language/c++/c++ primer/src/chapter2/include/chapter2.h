#pragma once
#include <iostream>
using namespace std;

namespace chapter2 {
    void stage1();
    inline void main() {
        cout << "------- chapter2 ------" << endl;
        stage1();
        cout << "======= chapter2 end =======" << endl;
    }
};
