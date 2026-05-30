# Java 语言详解

## 简介

Java 是一种高级、面向对象、静态类型的编程语言，由 Sun Microsystems 的 James Gosling 于 1995 年发布。Java 的设计哲学是"一次编写，到处运行"（Write Once, Run Anywhere），通过 JVM（Java 虚拟机）实现跨平台运行。

## 核心特点

- **跨平台**：JVM 实现平台无关性
- **面向对象**：严格的面向对象编程模型
- **静态类型**：编译时类型检查
- **自动内存管理**：垃圾回收机制
- **多线程**：内置多线程支持
- **强安全性**：安全管理器、字节码验证

## 语法示例

### 基础语法

```java
// 变量和数据类型
String name = "Java";
int version = 21;
double pi = 3.14159;
boolean isAwesome = true;
char letter = 'J';

// 数组
int[] numbers = {1, 2, 3, 4, 5};
String[] languages = {"Java", "Python", "Go"};

// 条件语句
if (version >= 21) {
    System.out.println("最新 LTS 版本");
} else if (version >= 17) {
    System.out.println("LTS 版本");
} else {
    System.out.println("旧版本");
}

// 循环
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}

for (int num : numbers) {
    System.out.println(num);
}
```

### 类和面向对象

```java
// 基类
public class Animal {
    private String name;
    private String sound;
    
    public Animal(String name, String sound) {
        this.name = name;
        this.sound = sound;
    }
    
    public String speak() {
        return name + " says " + sound + "!";
    }
    
    // Getter 和 Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}

// 继承
public class Dog extends Animal {
    public Dog(String name) {
        super(name, "Woof");
    }
    
    public String fetch(String item) {
        return getName() + " fetches the " + item;
    }
}

// 接口
public interface Pet {
    void play();
    default String getType() { return "Pet"; }
}

// 实现接口
public class Cat extends Animal implements Pet {
    public Cat(String name) {
        super(name, "Meow");
    }
    
    @Override
    public void play() {
        System.out.println(getName() + " plays with yarn");
    }
}
```

### Lambda 和函数式编程

```java
import java.util.*;
import java.util.stream.*;

// Lambda 表达式
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.forEach(name -> System.out.println(name));

// Stream API
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
int sum = numbers.stream()
    .filter(n -> n % 2 == 0)
    .mapToInt(n -> n * n)
    .sum();

// 方法引用
names.forEach(System.out::println);
```

### 异步编程

```java
import java.util.concurrent.*;

// CompletableFuture
public CompletableFuture<String> fetchData(String url) {
    return CompletableFuture.supplyAsync(() -> {
        // 模拟网络请求
        return "Data from " + url;
    });
}

// 使用
fetchData("https://api.example.com")
    .thenAccept(data -> System.out.println(data))
    .exceptionally(ex -> {
        System.out.println("Error: " + ex.getMessage());
        return null;
    });
```

## 优缺点

### 优点

- ✅ 跨平台性强（JVM）
- ✅ 成熟稳定，企业级应用首选
- ✅ 丰富的框架（Spring、Hibernate、Jakarta EE）
- ✅ 强大的 IDE 支持（IntelliJ IDEA、Eclipse）
- ✅ 完善的文档和社区
- ✅ 性能优秀（JIT 编译优化）

### 缺点

- ❌ 语法相对冗长
- ❌ 启动速度较慢
- ❌ 内存消耗较大
- ❌ 学习曲线较陡
- ❌ 不适合快速原型开发

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 企业级应用 | ERP、CRM、OA 系统 |
| Android 开发 | 原生 Android 应用 |
| 大数据处理 | Hadoop、Spark、Flink |
| Web 后端 | Spring Boot 微服务 |
| 金融系统 | 银行、证券交易平台 |
| 物联网 | 嵌入式系统、智能设备 |

## 学习资源

- Oracle Java 文档：https://docs.oracle.com/en/java/
- Baeldung：https://www.baeldung.com/
- LeetCode Java 题解：https://leetcode.cn/
- Spring 官方文档：https://spring.io/docs
