#include "chapter2.h"
#include <iostream>

namespace chapter2 {
    // struct Float {
    //     unsigned sign: 1;
    //     unsigned index : 8;
    //     unsigned base : 23;
    // };
    // Float 在内存中的保存形式
    struct Float {
        unsigned base : 23;  // 尾数
        unsigned index : 8;  // 指数
        unsigned sign: 1;    // 符号
    };

    void float_storge() {
        float test = -10.5;
        Float &pTest = (Float &)test;
        std::cout << sizeof(test) << std::endl; // 4        表示4*8 32位
        std::cout << pTest.sign << std::endl;   // 1        表示负数
        std::cout << pTest.index << std::endl;  // 130      表示指数是130-127=3
        std::cout << pTest.base << std::endl;   // 2621440  二进制为 010 1000 0000 0000 0000 0000共23位
        // base的范围是1 <= base < 2, 第一位必定为1，所以base的底数表示为1.010 1000 0000 0000 0000 0000
        // float -10.5 = -1.010 1000 0000 0000 0000 0000 * 2^3
        // (-1) * (2^0 + 2^-2 + 2^-4) * (2^3) = -1.3125 * 8 = -10.5
    }

    void stage1() {
        float_storge();
    }

}