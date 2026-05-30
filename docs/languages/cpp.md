# C++ 语言详解

## 简介

C++ 是一种通用的、静态类型的编程语言，由 Bjarne Stroustrup 于 1979 年在贝尔实验室开发。C++ 在 C 语言的基础上增加了面向对象、泛型编程等特性，是一种兼具底层控制和高级抽象的"零开销抽象"语言。

## 核心特点

- **多范式**：支持面向对象、泛型、函数式编程
- **零开销抽象**：高级特性不牺牲运行效率
- **RAII**：资源获取即初始化，自动资源管理
- **模板**：强大的编译时多态机制
- **STL**：标准模板库提供丰富的数据结构和算法
- **移动语义**：C++11 引入的所有权转移机制

## 语法示例

### 基础语法

```cpp
#include <iostream>
#include <vector>
#include <string>

// 变量和数据类型
std::string name = "C++";
int version = 23;
double pi = 3.141592653589793;
bool is_awesome = true;

// 数组和向量
int arr[] = {1, 2, 3, 4, 5};
std::vector<int> vec = {1, 2, 3, 4, 5};

// 条件语句
if (version >= 23) {
    std::cout << "最新版本" << std::endl;
} else if (version >= 11) {
    std::cout << "现代版本" << std::endl;
} else {
    std::cout << "旧版本" << std::endl;
}

// 循环
for (int i = 0; i < vec.size(); i++) {
    std::cout << vec[i] << " ";
}
std::cout << std::endl;

// 范围 for 循环
for (const auto& num : vec) {
    std::cout << num << " ";
}
```

### 类和面向对象

```cpp
#include <iostream>
#include <string>
#include <memory>

class Animal {
protected:
    std::string name;
    std::string sound;
    
public:
    Animal(std::string name, std::string sound) 
        : name(std::move(name)), sound(std::move(sound)) {}
    
    virtual ~Animal() = default;
    
    virtual std::string speak() const {
        return name + " says " + sound + "!";
    }
    
    const std::string& getName() const { return name; }
};

class Dog : public Animal {
public:
    Dog(std::string name) : Animal(std::move(name), "Woof") {}
    
    std::string fetch(const std::string& item) const {
        return name + " fetches the " + item;
    }
};

// 智能指针
auto dog = std::make_unique<Dog>("Buddy");
std::cout << dog->speak() << std::endl;
std::cout << dog->fetch("ball") << std::endl;
```

### 模板和泛型编程

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

// 函数模板
template<typename T>
T findMax(const std::vector<T>& vec) {
    return *std::max_element(vec.begin(), vec.end());
}

// 类模板
template<typename T>
class Stack {
private:
    std::vector<T> elements;
    
public:
    void push(const T& elem) {
        elements.push_back(elem);
    }
    
    T pop() {
        T elem = elements.back();
        elements.pop_back();
        return elem;
    }
    
    bool empty() const {
        return elements.empty();
    }
};

// 使用
Stack<int> intStack;
intStack.push(1);
intStack.push(2);
std::cout << intStack.pop() << std::endl;  // 2

std::vector<int> nums = {3, 1, 4, 1, 5};
std::cout << findMax(nums) << std::endl;  // 5
```

### Lambda 和函数式编程

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // Lambda 表达式
    auto isEven = [](int n) { return n % 2 == 0; };
    
    // 算法和 Lambda
    int count = std::count_if(nums.begin(), nums.end(), isEven);
    std::cout << "偶数个数: " << count << std::endl;
    
    // 排序
    std::sort(nums.begin(), nums.end(), [](int a, int b) {
        return a > b;  // 降序
    });
    
    // 函数对象
    std::function<int(int, int)> add = [](int a, int b) {
        return a + b;
    };
    std::cout << add(3, 4) << std::endl;  // 7
    
    return 0;
}
```

### 移动语义和智能指针

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Resource {
public:
    Resource() { std::cout << "Resource acquired" << std::endl; }
    ~Resource() { std::cout << "Resource released" << std::endl; }
    void use() { std::cout << "Resource used" << std::endl; }
};

int main() {
    // unique_ptr - 独占所有权
    auto ptr1 = std::make_unique<Resource>();
    ptr1->use();
    // auto ptr2 = ptr1;  // 错误！不能复制
    auto ptr2 = std::move(ptr1);  // 可以移动
    
    // shared_ptr - 共享所有权
    auto shared1 = std::make_shared<Resource>();
    auto shared2 = shared1;  // 引用计数增加
    std::cout << "引用计数: " << shared1.use_count() << std::endl;
    
    // weak_ptr - 弱引用
    std::weak_ptr<Resource> weak = shared1;
    if (auto locked = weak.lock()) {
        locked->use();
    }
    
    return 0;
}
```

## 优缺点

### 优点

- ✅ 性能极高，接近 C 语言
- ✅ 强大的抽象能力
- ✅ 丰富的标准库（STL）
- ✅ 跨平台支持
- ✅ 适合系统级编程
- ✅ 模板元编程能力强大

### 缺点

- ❌ 学习曲线陡峭
- ❌ 编译时间长
- ❌ 语法复杂
- ❌ 内存安全问题（虽有 RAII 但仍需注意）
- ❌ 头文件机制繁琐

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 游戏开发 | Unreal Engine、游戏引擎 |
| 系统软件 | 操作系统、驱动程序 |
| 高性能计算 | 科学计算、数值模拟 |
| 图形渲染 | OpenGL、Vulkan |
| 嵌入式系统 | 资源受限环境 |
| 金融系统 | 高频交易平台 |

## 学习资源

- C++ 官方文档：https://cppreference.com/
- LearnCpp：https://www.learncpp.com/
- C++ Core Guidelines：https://isocpp.github.io/CppCoreGuidelines/
- Godbolt 编译器：https://godbolt.org/
