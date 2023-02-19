#include "chapter1.h"

namespace chapter1 {
    void a1_3() {
        cout << "Hello World!" << endl;
    }

    int add(int a, int b) {
        return a + b;
    }

    int mul(int a, int b) {
        return a * b;
    }

    void a1_4() {
        cout << add(1, 2) << endl;
        cout << mul(3, 4) << endl;
    }

    void a1_5() {
        cout << 1 << 2 << endl;
    }

    void a1_6() {
        // 不合法 第2，3行没有对象进行定向，已经使用分号隔开，属于独立的语句。
    }

    void c1_2() {
        a1_3();
        a1_4();
        a1_5();
    }


    // 1.3
    void a1_7() {
        // /* test 
        // /* */
        // */
        // 无法嵌套注释
    }

    void a1_8() {
        cout << "/*";
        cout << "*/";
        // cout << /* "*/" */;
        cout << /* "*/" /* "/*" */;
    }

    void c1_3() {
        a1_8();
    }

    void stage1() {
         cout << "chapter1 stage1" << endl;
        //  c1_2();
         c1_3();
    }
}