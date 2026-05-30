# Go 语言详解

## 简介

Go（又称 Golang）是一种静态类型、编译型的编程语言，由 Google 的 Robert Griesemer、Rob Pike 和 Ken Thompson 于 2009 年发布。Go 语言以简洁、高效和并发友好著称，特别适合构建高性能的网络服务和分布式系统。

## 核心特点

- **简洁设计**：语法简洁，只有 25 个关键字
- **并发原生**：goroutine 和 channel 实现轻量级并发
- **快速编译**：编译速度极快
- **静态链接**：编译后生成单一可执行文件
- **垃圾回收**：自动内存管理
- **强类型**：静态类型系统，编译时类型检查

## 语法示例

### 基础语法

```go
package main

import "fmt"

func main() {
    // 变量声明
    var name string = "Go"
    version := 1.21  // 短变量声明
    
    // 常量
    const Pi = 3.14159
    
    // 基本类型
    var (
        intVal    int     = 42
        floatVal  float64 = 3.14
        boolVal   bool    = true
        stringVal string  = "hello"
    )
    
    // 数组和切片
    arr := [5]int{1, 2, 3, 4, 5}
    slice := []int{1, 2, 3, 4, 5}
    slice = append(slice, 6)
    
    // 映射
    m := map[string]int{
        "one":   1,
        "two":   2,
        "three": 3,
    }
    
    // 条件语句
    if version >= 1.21 {
        fmt.Println("最新版本")
    } else if version >= 1.18 {
        fmt.Println("支持泛型的版本")
    } else {
        fmt.Println("旧版本")
    }
    
    // 循环
    for i := 0; i < len(slice); i++ {
        fmt.Println(slice[i])
    }
    
    // 范围循环
    for i, v := range slice {
        fmt.Printf("索引: %d, 值: %d\n", i, v)
    }
}
```

### 函数

```go
package main

import "fmt"

// 基础函数
func add(a, b int) int {
    return a + b
}

// 多返回值
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("除数不能为零")
    }
    return a / b, nil
}

// 命名返回值
func swap(a, b int) (x, y int) {
    x = b
    y = a
    return
}

// 可变参数
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// 函数作为参数
func apply(nums []int, fn func(int) int) []int {
    result := make([]int, len(nums))
    for i, n := range nums {
        result[i] = fn(n)
    }
    return result
}

func main() {
    fmt.Println(add(3, 4))
    
    result, err := divide(10, 3)
    if err != nil {
        fmt.Println("错误:", err)
    } else {
        fmt.Println("结果:", result)
    }
    
    fmt.Println(sum(1, 2, 3, 4, 5))
    
    doubles := apply([]int{1, 2, 3}, func(n int) int {
        return n * 2
    })
    fmt.Println(doubles)
}
```

### 结构体和接口

```go
package main

import "fmt"

// 结构体
type Animal struct {
    Name  string
    Sound string
}

func (a Animal) Speak() string {
    return a.Name + " says " + a.Sound + "!"
}

// 继承（组合）
type Dog struct {
    Animal
}

func (d Dog) Fetch(item string) string {
    return d.Name + " fetches the " + item
}

// 接口
type Speaker interface {
    Speak() string
}

type Pet interface {
    Speaker
    Play()
}

// 实现接口
type Cat struct {
    Name string
}

func (c Cat) Speak() string {
    return c.Name + " says Meow!"
}

func (c Cat) Play() {
    fmt.Println(c.Name + " plays with yarn")
}

func main() {
    dog := Dog{Animal{"Buddy", "Woof"}}
    fmt.Println(dog.Speak())
    fmt.Println(dog.Fetch("ball"))
    
    var speaker Speaker = Cat{"Kitty"}
    fmt.Println(speaker.Speak())
    
    var pet Pet = Cat{"Kitty"}
    pet.Play()
}
```

### 并发编程

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Goroutine 和 Channel
func producer(ch chan<- int) {
    for i := 0; i < 5; i++ {
        ch <- i
        time.Sleep(100 * time.Millisecond)
    }
    close(ch)
}

func consumer(ch <-chan int, wg *sync.WaitGroup) {
    defer wg.Done()
    for v := range ch {
        fmt.Println("收到:", v)
    }
}

// 使用 WaitGroup
func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Printf("工人 %d 开始工作\n", id)
    time.Sleep(time.Second)
    fmt.Printf("工人 %d 完成工作\n", id)
}

func main() {
    // Channel 示例
    ch := make(chan int)
    go producer(ch)
    
    var wg sync.WaitGroup
    wg.Add(1)
    go consumer(ch, &wg)
    wg.Wait()
    
    // WaitGroup 示例
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, &wg)
    }
    wg.Wait()
    
    fmt.Println("所有工作完成")
}
```

## 优缺点

### 优点

- ✅ 编译速度快
- ✅ 并发编程简单高效
- ✅ 部署方便（单一二进制文件）
- ✅ 语法简洁易学
- ✅ 强大的标准库
- ✅ 垃圾回收

### 缺点

- ❌ 错误处理繁琐
- ❌ 缺乏泛型（1.18 后已支持）
- ❌ 包管理机制不够完善
- ❌ 缺少某些高级语言特性
- ❌ 社区生态相对较新

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 云原生开发 | Docker、Kubernetes |
| 微服务 | 高性能 API 网关 |
| 网络编程 | Web 服务器、代理 |
| 命令行工具 | CLI 应用开发 |
| 区块链 | 以太坊 Geth |
| 分布式系统 | 消息队列、存储系统 |

## 学习资源

- Go 官方文档：https://go.dev/doc/
- Go by Example：https://gobyexample.com/
- Go Tour：https://go.dev/tour/
- Effective Go：https://go.dev/doc/effective_go
