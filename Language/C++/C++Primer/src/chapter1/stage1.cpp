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

    // 1.4.1
    void a1_9() {
        int sum = 0;
        int a = 50;
        while (a <= 100) {
            sum += a;
            a++;
        }
        cout << sum << endl;
    }

    void a1_10() {
        int a = 10;
        while (a >= 0) {
            cout << a-- << endl;
        }
    }

    void a1_11() {
        cout << "Input small num then large:";
        int a, b;
        cin >> a >> b;
        while (a <= b) {
            cout << a++ << endl;
        }
    }

    void c1_4_1() {
        a1_9();
        a1_10();
        a1_11();
    }

    // 1.4.2
    void a1_12() {
        // -100 到 100的和
        // 结果为0
    }

    void a1_13() {
        // 1.9
        int sum = 0;
        for (int i = 50; i <= 100; i++) {
            sum += i;
        }
        cout << sum << endl;
        // 1.10
        for (int i = 10; i >=0; i--) {
            cout << i << endl;
        }
        int a, b;
        cout << "Enter num:";
        cin >> a >> b;
        for (int i = a; i <= b; i++) {
            cout << i << endl;
        }
    }

    void c1_4_2() {
        a1_13();
    }


    void stage1() {
         cout << "chapter1 stage1" << endl;
        //  c1_2();
        //  c1_3();
         c1_4_1();
    }
}