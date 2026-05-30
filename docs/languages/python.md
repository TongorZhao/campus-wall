# Python 语言详解

## 简介

Python 是一种高级、解释型、通用的编程语言，由 Guido van Rossum 于 1991 年发布。Python 的设计哲学强调代码的可读性和简洁性，使用缩进来定义代码块。

## 核心特点

- **简洁优雅**：语法简洁清晰，接近自然语言
- **动态类型**：变量不需要声明类型
- **解释执行**：无需编译，直接运行
- **丰富的库**：拥有庞大的标准库和第三方库生态
- **跨平台**：支持 Windows、macOS、Linux 等操作系统
- **多范式**：支持面向对象、函数式、过程式编程

## 语法示例

### 基础语法

```python
# 变量和数据类型
name = "Python"
version = 3.11
is_awesome = True
languages = ["Python", "JavaScript", "Go"]

# 条件语句
if version >= 3.11:
    print(f"{name} {version} 是最新版本")
elif version >= 3.0:
    print(f"{name} 3.x 版本")
else:
    print(f"{name} 2.x 版本")

# 循环
for lang in languages:
    print(lang)

# 列表推导式
squares = [x**2 for x in range(10)]
```

### 函数定义

```python
# 基础函数
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Lambda 函数
add = lambda x, y: x + y

# 装饰器
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"执行时间: {time.time() - start:.2f}秒")
        return result
    return wrapper
```

### 类和面向对象

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
    
    def speak(self):
        return f"{self.name} says {self.sound}!"

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")
    
    def fetch(self, item):
        return f"{self.name} fetches the {item}"

# 使用
dog = Dog("Buddy")
print(dog.speak())  # Buddy says Woof!
print(dog.fetch("ball"))  # Buddy fetches the ball
```

### 异步编程

```python
import asyncio

async def fetch_data(url):
    print(f"开始获取 {url}")
    await asyncio.sleep(1)  # 模拟网络请求
    return f"{url} 的数据"

async def main():
    tasks = [
        fetch_data("https://api.example.com/users"),
        fetch_data("https://api.example.com/posts"),
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

## 优缺点

### 优点

- ✅ 学习曲线平缓，易于上手
- ✅ 代码可读性强，维护成本低
- ✅ 丰富的生态系统（NumPy、Pandas、Django、Flask）
- ✅ 强大的社区支持
- ✅ 适合快速原型开发
- ✅ 在数据科学、AI 领域占据主导地位

### 缺点

- ❌ 执行速度相对较慢（解释型语言）
- ❌ GIL（全局解释器锁）限制了多线程性能
- ❌ 移动端开发支持较弱
- ❌ 内存消耗较大

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 数据科学 | 数据分析、数据可视化、统计建模 |
| 人工智能/机器学习 | 深度学习、自然语言处理、计算机视觉 |
| Web 开发 | 后端服务、API 开发（Django、Flask） |
| 自动化脚本 | 系统管理、爬虫、批处理 |
| 科学计算 | 数学建模、仿真模拟 |
| 物联网 | 树莓派开发、传感器数据处理 |

## 学习资源

- 官方文档：https://docs.python.org/
- Python 教程：https://docs.python.org/3/tutorial/
- Real Python：https://realpython.com/
- LeetCode Python 题解：https://leetcode.cn/
