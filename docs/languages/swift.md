# Swift 语言详解

## 简介

Swift 是由 Apple 开发的现代编程语言，于 2014 年发布。Swift 设计目标是成为 Objective-C 的替代品，同时提供更安全、更现代的编程体验。Swift 可用于开发 iOS、macOS、watchOS、tvOS 和 Linux 应用。

## 核心特点

- **安全性强**：类型安全、空值安全、内存安全
- **性能优秀**：编译优化，接近 C++ 性能
- **现代语法**：简洁清晰，易于阅读
- **协议导向**：强调协议和组合而非继承
- **互操作性**：与 Objective-C 完全兼容
- **跨平台**：支持 macOS、iOS、Linux、Windows

## 语法示例

### 基础语法

```swift
import Foundation

// 变量和常量
let name = "Swift"  // 常量
var version = 5.9    // 变量

// 数据类型
let integer: Int = 42
let double: Double = 3.14159
let string: String = "Hello"
let boolean: Bool = true

// 类型推断
let inferredInt = 100
let inferredDouble = 3.14
let inferredString = "World"

// 可选类型
var optionalString: String? = "Hello"
var nilValue: String? = nil

// 数组
let numbers = [1, 2, 3, 4, 5]
var mutableNumbers = [1, 2, 3]
mutableNumbers.append(4)

// 字典
let person = ["name": "Alice", "city": "Beijing"]
var scores = ["Alice": 95, "Bob": 87]

// 集合
let uniqueNumbers: Set = [1, 2, 3, 3, 4]  // {1, 2, 3, 4}

// 条件语句
if version >= 5.9 {
    print("最新版本")
} else if version >= 5.0 {
    print("现代版本")
} else {
    print("旧版本")
}

// 循环
for number in numbers {
    print(number)
}

for i in 0..<5 {
    print(i)
}

for (name, score) in scores {
    print("\(name): \(score)")
}
```

### 函数和闭包

```swift
// 基础函数
func add(a: Int, b: Int) -> Int {
    return a + b
}

// 参数标签
func greet(person name: String, from city: String) -> String {
    return "Hello \(name) from \(city)!"
}

// 默认参数
func power(_ base: Int, exponent: Int = 2) -> Int {
    return Int(pow(Double(base), Double(exponent)))
}

// 返回多个值
func minMax(_ array: [Int]) -> (min: Int, max: Int)? {
    guard let first = array.first else { return nil }
    var min = first, max = first
    for value in array {
        if value < min { min = value }
        if value > max { max = value }
    }
    return (min, max)
}

// 可变参数
func average(_ numbers: Double...) -> Double {
    let total = numbers.reduce(0, +)
    return total / Double(numbers.count)
}

// 使用
let sum = add(a: 3, b: 4)
print(greet(person: "Alice", from: "Beijing"))
print(power(2, exponent: 10))
print(average(1, 2, 3, 4, 5))

// 闭包
let numbers = [5, 3, 1, 4, 2]
let sorted = numbers.sorted { $0 < $1 }
let doubled = numbers.map { $0 * 2 }
let evens = numbers.filter { $0 % 2 == 0 }
let sum = numbers.reduce(0, +)
```

### 类和面向对象

```swift
// 协议
protocol Shape {
    var area: Double { get }
    var perimeter: Double { get }
    func describe() -> String
}

// 类
class Animal {
    var name: String
    var sound: String
    
    init(name: String, sound: String) {
        self.name = name
        self.sound = sound
    }
    
    func speak() -> String {
        return "\(name) says \(sound)!"
    }
    
    deinit {
        print("\(name) is being deallocated")
    }
}

// 继承
class Dog: Animal {
    var breed: String
    
    init(name: String, breed: String) {
        self.breed = breed
        super.init(name: name, sound: "Woof")
    }
    
    func fetch(item: String) -> String {
        return "\(name) fetches the \(item)"
    }
}

// 实现协议
class Circle: Shape {
    let radius: Double
    
    init(radius: Double) {
        self.radius = radius
    }
    
    var area: Double {
        return .pi * radius * radius
    }
    
    var perimeter: Double {
        return 2 * .pi * radius
    }
    
    func describe() -> String {
        return "Circle with radius \(radius)"
    }
}

// 结构体
struct Point {
    var x: Double
    var y: Double
    
    func distance(to other: Point) -> Double {
        let dx = x - other.x
        let dy = y - other.y
        return sqrt(dx * dx + dy * dy)
    }
}

// 使用
let dog = Dog(name: "Buddy", breed: "Golden Retriever")
print(dog.speak())
print(dog.fetch(item: "ball"))

let circle = Circle(radius: 5)
print("面积: \(circle.area)")

let p1 = Point(x: 0, y: 0)
let p2 = Point(x: 3, y: 4)
print("距离: \(p1.distance(to: p2))")
```

### 错误处理

```swift
// 定义错误
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
    case serverError(statusCode: Int)
}

// 抛出错误
func fetchData(from urlString: String) throws -> Data {
    guard let url = URL(string: urlString) else {
        throw NetworkError.invalidURL
    }
    
    let data = try Data(contentsOf: url)
    guard !data.isEmpty else {
        throw NetworkError.noData
    }
    
    return data
}

// 处理错误
do {
    let data = try fetchData(from: "https://api.example.com")
    print("获取到 \(data.count) 字节")
} catch NetworkError.invalidURL {
    print("URL 无效")
} catch NetworkError.serverError(let statusCode) {
    print("服务器错误: \(statusCode)")
} catch {
    print("未知错误: \(error)")
}

// Result 类型
func divide(_ a: Double, by b: Double) -> Result<Double, Error> {
    guard b != 0 else {
        return .failure(NSError(domain: "Math", code: 1, userInfo: [NSLocalizedDescriptionKey: "除数不能为零"]))
    }
    return .success(a / b)
}

let result = divide(10, by: 3)
switch result {
case .success(let value):
    print("结果: \(value)")
case .failure(let error):
    print("错误: \(error)")
}
```

### 现代 Swift 特性

```swift
// 属性包装器
@propertyWrapper
struct Clamped {
    private var value: Int
    let range: ClosedRange<Int>
    
    var wrappedValue: Int {
        get { value }
        set { value = min(max(range.lowerBound, newValue), range.upperBound) }
    }
    
    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.value = min(max(range.lowerBound, wrappedValue), range.upperBound)
    }
}

// 使用
struct Player {
    @Clamped(0...100) var health = 100
    @Clamped(0...999) var score = 0
}

// Codable
struct User: Codable {
    let name: String
    let age: Int
    let email: String?
}

let json = """
{"name": "Alice", "age": 30}
""".data(using: .utf8)!

let user = try JSONDecoder().decode(User.self, from: json)
print(user.name)

// async/await
func fetchUser() async throws -> User {
    let url = URL(string: "https://api.example.com/user")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// 结果构建器
@resultBuilder
struct ArrayBuilder {
    static func buildBlock(_ components: Int...) -> [Int] {
        components
    }
}

@ArrayBuilder
func makeArray() -> [Int] {
    1
    2
    3
}
```

## 优缺点

### 优点

- ✅ 现代、安全的语法
- ✅ 性能优秀
- ✅ Apple 生态系统的首选语言
- ✅ 强大的类型系统
- ✅ 协议导向编程
- ✅ 活跃的社区

### 缺点

- ❌ 主要局限于 Apple 平台
- ❌ 学习曲线（对非程序员）
- ❌ 某些高级特性较复杂
- ❌ Linux/Windows 支持相对较新
- ❌ 编译速度有时较慢

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| iOS 开发 | iPhone、iPad 应用 |
| macOS 开发 | 桌面应用程序 |
| watchOS | Apple Watch 应用 |
| tvOS | Apple TV 应用 |
| 服务器端 | Vapor、Kitura |
| 命令行工具 | Swift CLI 应用 |

## 学习资源

- Swift 官方文档：https://docs.swift.org/swift-book/
- Swift Playgrounds：Apple 官方学习应用
- Hacking with Swift：https://www.hackingwithswift.com/
- Swift by Sundell：https://www.swiftbysundell.com/
