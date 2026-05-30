# Rust 语言详解

## 简介

Rust 是一种系统级编程语言，由 Mozilla 的 Graydon Hoare 于 2006 年设计，2015 年发布 1.0 版本。Rust 以"安全、并发、高性能"为核心目标，通过所有权系统在编译时保证内存安全，无需垃圾回收。

## 核心特点

- **内存安全**：所有权系统防止空指针、悬垂引用
- **零成本抽象**：高级特性不牺牲运行效率
- **并发安全**：编译时防止数据竞争
- **模式匹配**：强大的枚举和匹配表达式
- **trait 系统**：灵活的接口和多态机制
- **Cargo**：优秀的包管理和构建工具

## 语法示例

### 基础语法

```rust
fn main() {
    // 变量绑定
    let name = "Rust";
    let version = 1.75;
    let is_awesome = true;
    
    // 可变性
    let mut count = 0;
    count += 1;
    
    // 常量
    const MAX_SIZE: u32 = 1000;
    
    // 数组和切片
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4];
    
    // 向量
    let mut vec = vec![1, 2, 3];
    vec.push(4);
    
    // 元组
    let person = ("Alice", 30);
    let (name, age) = person;
    
    // 条件语句
    if version >= 1.75 {
        println!("最新版本");
    } else if version >= 1.56 {
        println!("稳定版本");
    } else {
        println!("旧版本");
    }
    
    // 循环
    for i in 0..5 {
        println!("{}", i);
    }
    
    // while 循环
    let mut x = 0;
    while x < 5 {
        println!("{}", x);
        x += 1;
    }
    
    // loop 循环
    let mut y = 0;
    loop {
        if y >= 3 { break; }
        println!("{}", y);
        y += 1;
    }
}
```

### 函数

```rust
// 基础函数
fn add(a: i32, b: i32) -> i32 {
    a + b  // 最后一个表达式作为返回值
}

// 多返回值
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("除数不能为零".to_string())
    } else {
        Ok(a / b)
    }
}

// 函数作为参数
fn apply<F: Fn(i32) -> i32>(nums: Vec<i32>, f: F) -> Vec<i32> {
    nums.iter().map(|&n| f(n)).collect()
}

// 闭包
fn main() {
    let result = add(3, 4);
    println!("3 + 4 = {}", result);
    
    match divide(10.0, 3.0) {
        Ok(result) => println!("结果: {:.2}", result),
        Err(e) => println!("错误: {}", e),
    }
    
    let nums = vec![1, 2, 3, 4, 5];
    let doubled = apply(nums, |n| n * 2);
    println!("{:?}", doubled);
    
    // 所有权和借用
    let s1 = String::from("hello");
    let s2 = s1.clone();  // 深拷贝
    println!("s1 = {}, s2 = {}", s1, s2);
    
    let s3 = &s1;  // 不可变借用
    println!("s3 = {}", s3);
}
```

### 结构体和枚举

```rust
// 结构体
#[derive(Debug)]
struct Animal {
    name: String,
    sound: String,
}

impl Animal {
    fn new(name: &str, sound: &str) -> Self {
        Animal {
            name: name.to_string(),
            sound: sound.to_string(),
        }
    }
    
    fn speak(&self) -> String {
        format!("{} says {}!", self.name, self.sound)
    }
}

// 继承（通过 trait）
trait Pet {
    fn play(&self);
}

#[derive(Debug)]
struct Dog {
    animal: Animal,
}

impl Dog {
    fn new(name: &str) -> Self {
        Dog {
            animal: Animal::new(name, "Woof"),
        }
    }
    
    fn fetch(&self, item: &str) -> String {
        format!("{} fetches the {}", self.animal.name, item)
    }
}

impl Pet for Dog {
    fn play(&self) {
        println!("{} plays fetch!", self.animal.name);
    }
}

// 枚举
#[derive(Debug)]
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn process_message(msg: Message) {
    match msg {
        Message::Quit => println!("退出"),
        Message::Move { x, y } => println!("移动到 ({}, {})", x, y),
        Message::Write(text) => println!("写入: {}", text),
        Message::ChangeColor(r, g, b) => println!("改变颜色: ({}, {}, {})", r, g, b),
    }
}

fn main() {
    let dog = Dog::new("Buddy");
    println!("{}", dog.animal.speak());
    println!("{}", dog.fetch("ball"));
    dog.play();
    
    let msg = Message::Write("Hello".to_string());
    process_message(msg);
}
```

### 错误处理

```rust
use std::fs;
use std::io;

// 自定义错误
#[derive(Debug)]
enum AppError {
    IoError(io::Error),
    ParseError(std::num::ParseIntError),
    CustomError(String),
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::IoError(error)
    }
}

impl From<std::num::ParseIntError> for AppError {
    fn from(error: std::num::ParseIntError) -> Self {
        AppError::ParseError(error)
    }
}

// 使用 Result 和 ? 操作符
fn read_number_from_file(path: &str) -> Result<i32, AppError> {
    let content = fs::read_to_string(path)?;
    let number: i32 = content.trim().parse()?;
    Ok(number)
}

// Option 类型
fn find_first_even(numbers: &[i32]) -> Option<i32> {
    for &num in numbers {
        if num % 2 == 0 {
            return Some(num);
        }
    }
    None
}

fn main() {
    match read_number_from_file("number.txt") {
        Ok(n) => println!("读取到: {}", n),
        Err(e) => println!("错误: {:?}", e),
    }
    
    let numbers = vec![1, 3, 5, 8, 9];
    match find_first_even(&numbers) {
        Some(n) => println!("第一个偶数: {}", n),
        None => println!("没有偶数"),
    }
}
```

## 优缺点

### 优点

- ✅ 内存安全，无需垃圾回收
- ✅ 性能接近 C/C++
- ✅ 出色的并发安全性
- ✅ 优秀的工具链（Cargo、rustfmt、clippy）
- ✅ 活跃的社区
- ✅ 适合系统级编程

### 缺点

- ❌ 学习曲线陡峭（所有权系统）
- ❌ 编译时间较长
- ❌ 生态系统相对较小
- ❌ 异步编程较复杂
- ❌ 不适合快速原型开发

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 系统编程 | 操作系统、驱动程序 |
| WebAssembly | 浏览器端高性能计算 |
| 命令行工具 | ripgrep、fd、bat |
| 网络服务 | 高性能 API 服务 |
| 嵌入式系统 | IoT 设备开发 |
| 区块链 | Solana、Polkadot |

## 学习资源

- Rust 官方文档：https://doc.rust-lang.org/
- Rust Book：https://doc.rust-lang.org/book/
- Rust by Example：https://doc.rust-lang.org/rust-by-example/
- Rustlings：https://github.com/rust-lang/rustlings
