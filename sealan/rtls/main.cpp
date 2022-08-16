#include <iostream>
// 包含了头文件，这里面包含程序必须的或有用的信息，vec3d结构就在这里面定义了
#include "trilateration.h"

// 告诉编译器使用 std 命名空间。命名空间是 C++ 中一个相对新的概念
using namespace std;
// main() 是程序开始执行的地方
int main() {
    // 定义初始化result int = 0
	int result = 0;

    // 数组，三维坐标
	vec3d anchorArray[3];
    // 声明一个int数组，大小3
	int distanceArray[3];
    // 三个点的距离
	distanceArray[0] = 2910;
	distanceArray[1] = 2760;
	distanceArray[2] = 2630;

    // 三个点的坐标，z统一为0
	anchorArray[0].x = 0;
	anchorArray[0].y = 0;
	anchorArray[0].z = 0;

	anchorArray[1].x = 4;
	anchorArray[1].y = 4;
	anchorArray[1].z = 0;

	anchorArray[2].x = 0;
	anchorArray[2].y = 4;
	anchorArray[2].z = 0;

    // 声明一个三维坐标
	vec3d report;

    // 求坐标函数，
    // report 空三维坐标，用来填计算结果， 
    //  &anchorArray[0]  怎么只提交一个坐标，应该是提交一个坐标的指针，后面的就都能获取到
    // 三点距离
	result = GetLocation(&report, 1, &anchorArray[0], distanceArray);
	
    // 打印目标点坐标
    //  endl英语意思是end of line,即一行输出结束，然后输出下一行。
	cout << endl;
	cout << report.x << endl;
	cout << report.y << endl;
	cout << report.z << endl;
	//cout << "This is a C++ program.";
    // 终止程序
	return 0;
}