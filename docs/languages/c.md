# C 语言详解

## 简介

C 语言是一种通用的、过程式的编程语言，由 Dennis Ritchie 于 1972 年在贝尔实验室开发。C 语言是现代编程语言的基石，影响了 C++、Java、C# 等众多语言，被誉为"编程语言之母"。

## 核心特点

- **接近硬件**：可直接操作内存和硬件资源
- **高效执行**：编译后直接运行，性能极高
- **可移植性**：标准 C 可在多种平台编译
- **简洁语法**：关键字少，语法精炼
- **指针操作**：直接内存寻址能力
- **结构化编程**：支持函数、结构体等模块化设计

## 语法示例

### 基础语法

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 变量和数据类型
char name[] = "C";
int version = 11;
float pi = 3.14159f;
double precision = 3.141592653589793;
unsigned int positive = 42;

// 数组
int numbers[] = {1, 2, 3, 4, 5};
int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

// 条件语句
if (version >= 11) {
    printf("最新版本\n");
} else if (version >= 9) {
    printf("现代版本\n");
} else {
    printf("旧版本\n");
}

// 循环
for (int i = 0; i < 5; i++) {
    printf("%d ", numbers[i]);
}
printf("\n");
```

### 函数

```c
// 函数声明
int add(int a, int b);
void swap(int *a, int *b);
int factorial(int n);

// 函数定义
int add(int a, int b) {
    return a + b;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

### 指针和内存

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 指针基础
    int x = 10;
    int *ptr = &x;
    printf("x 的值: %d\n", x);
    printf("x 的地址: %p\n", (void*)ptr);
    printf("通过指针访问: %d\n", *ptr);
    
    // 动态内存分配
    int *arr = (int*)malloc(5 * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return 1;
    }
    
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 2;
    }
    
    // 释放内存
    free(arr);
    arr = NULL;
    
    return 0;
}
```

### 结构体和链表

```c
#include <stdio.h>
#include <stdlib.h>

// 结构体定义
typedef struct Node {
    int data;
    struct Node *next;
} Node;

// 创建节点
Node* createNode(int data) {
    Node *newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// 链表操作
void push(Node **head, int data) {
    Node *newNode = createNode(data);
    newNode->next = *head;
    *head = newNode;
}

void printList(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

// 释放链表
void freeList(Node *head) {
    Node *temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}
```

### 文件操作

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file;
    char buffer[256];
    
    // 写入文件
    file = fopen("example.txt", "w");
    if (file == NULL) {
        perror("无法打开文件");
        return 1;
    }
    fprintf(file, "Hello, C!\n");
    fclose(file);
    
    // 读取文件
    file = fopen("example.txt", "r");
    if (file == NULL) {
        perror("无法打开文件");
        return 1;
    }
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }
    fclose(file);
    
    return 0;
}
```

## 优缺点

### 优点

- ✅ 执行效率极高
- ✅ 可直接操作硬件
- ✅ 内存使用精细控制
- ✅ 编译后体积小
- ✅ 语言标准稳定
- ✅ 嵌入式系统首选

### 缺点

- ❌ 手动内存管理容易出错
- ❌ 没有内置的面向对象支持
- ❌ 缺乏现代语言特性（如泛型）
- ❌ 安全性问题（缓冲区溢出）
- ❌ 开发效率相对较低

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 操作系统 | Linux、Windows 内核 |
| 嵌入式系统 | 单片机、RTOS |
| 数据库 | MySQL、PostgreSQL |
| 编译器 | GCC、LLVM |
| 游戏引擎 | 底层图形渲染 |
| 驱动程序 | 设备驱动开发 |

## 学习资源

- C 语言中文网：https://www.runoob.com/cprogramming/c-tutorial.html
- C Primer Plus：经典教材
- Learn C：https://www.learn-c.org/
- C FAQ：https://c-faq.com/
