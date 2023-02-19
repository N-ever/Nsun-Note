#include "algorithm.h"
#include <iostream>
#include <random>

using namespace std;

namespace algorithm {
    void sort(int * arr, int firstIndex, int lastIndex) {
        if (lastIndex <= firstIndex) return;
        int pivot = arr[firstIndex];
        cout << pivot << endl;
        int left = firstIndex;
        int right = lastIndex;
        int index = left;
        while (right > left) {
            while (right > left) {
                if (arr[right] < pivot) {
                    arr[left] = arr[right];
                    index = right; 
                    left++;
                    break;
                }
                right--;
            }
            while (right> left) {
                if (arr[left] >  pivot) {
                    arr[right] = arr[left];
                    index = left;
                    right--;
                    break; 
                }
                left++;
            }
            arr[index] = pivot;
        }
        sort(arr, firstIndex, index);
        sort(arr, index + 1, lastIndex);
    }

    void fast_sort() {
        static int ARR_NUM = 10;
        int test[ARR_NUM];
        for (int i = 0; i < ARR_NUM; i++) {
            test[i] = rand() % 10000;
            cout << test[i] << " ";
        }
        cout << endl;
        sort(test, 0, ARR_NUM - 1);
        for (int i = 0; i < ARR_NUM; i++) {
            cout << test[i] << " ";
        }
        cout << endl;
    }
}