# JavaScript 语言详解

## 简介

JavaScript 是一种高级、解释型、动态类型的编程语言，最初由 Brendan Eich 于 1995 年创建，用于为网页添加交互功能。如今 JavaScript 已经发展成为全栈开发语言，可在浏览器和服务器端（Node.js）运行。

## 核心特点

- **事件驱动**：基于事件循环的异步编程模型
- **函数式编程**：支持高阶函数、闭包等函数式特性
- **原型继承**：基于原型的面向对象系统
- **动态类型**：变量类型在运行时确定
- **单线程异步**：通过事件循环实现非阻塞 I/O
- **跨平台**：浏览器、服务器、移动应用、桌面应用

## 语法示例

### 基础语法

```javascript
// 变量声明
const name = "JavaScript";  // 常量
let version = 15;           // 可变变量
var oldWay = "不推荐使用";   // 旧语法

// 数据类型
const string = "Hello";
const number = 42;
const boolean = true;
const array = [1, 2, 3];
const object = { key: "value" };
const nullValue = null;
const undefinedValue = undefined;

// 条件语句
if (version >= 15) {
    console.log("最新版本");
} else if (version >= 6) {
    console.log("现代版本");
} else {
    console.log("旧版本");
}

// 循环
for (let i = 0; i < array.length; i++) {
    console.log(array[i]);
}

array.forEach(item => console.log(item));
```

### 函数

```javascript
// 函数声明
function greet(name) {
    return `Hello, ${name}!`;
}

// 箭头函数
const add = (a, b) => a + b;

// 高阶函数
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);

// 闭包
function createCounter() {
    let count = 0;
    return {
        increment: () => ++count,
        getCount: () => count
    };
}
```

### 类和面向对象

```javascript
class Animal {
    constructor(name, sound) {
        this.name = name;
        this.sound = sound;
    }
    
    speak() {
        return `${this.name} says ${this.sound}!`;
    }
    
    static create(name, sound) {
        return new Animal(name, sound);
    }
}

class Dog extends Animal {
    constructor(name) {
        super(name, "Woof");
    }
    
    fetch(item) {
        return `${this.name} fetches the ${item}`;
    }
}

const dog = new Dog("Buddy");
console.log(dog.speak());  // Buddy says Woof!
```

### 异步编程

```javascript
// Promise
function fetchData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(`Data from ${url}`);
        }, 1000);
    });
}

// async/await
async function getData() {
    try {
        const data = await fetchData("https://api.example.com");
        console.log(data);
    } catch (error) {
        console.error("Error:", error);
    }
}

// 并发请求
async function fetchMultiple() {
    const [users, posts] = await Promise.all([
        fetchData("/users"),
        fetchData("/posts")
    ]);
    return { users, posts };
}
```

### ES6+ 新特性

```javascript
// 解构赋值
const { name, version } = { name: "JS", version: 15 };
const [first, second, ...rest] = [1, 2, 3, 4, 5];

// 展开运算符
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };

// 模板字符串
const message = `Hello, ${name}! Version: ${version}`;

// 可选链
const user = { profile: { name: "John" } };
const userName = user?.profile?.name;

// 空值合并
const value = null ?? "default";  // "default"
```

## 优缺点

### 优点

- ✅ 无处不在，浏览器原生支持
- ✅ 丰富的生态系统（npm 拥有百万级包）
- ✅ 前后端统一语言（Node.js）
- ✅ 即时反馈，开发效率高
- ✅ 强大的社区和框架（React、Vue、Angular）
- ✅ 事件驱动适合高并发场景

### 缺点

- ❌ 类型系统较弱（TypeScript 可以解决）
- ❌ 浏览器兼容性问题
- ❌ 回调地狱（async/await 可以解决）
- ❌ 单线程限制 CPU 密集型任务
- ❌ 语言规范变化快，学习成本高

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 前端开发 | 单页应用、移动响应式网站 |
| 后端开发 | Node.js 服务器、API 服务 |
| 移动应用 | React Native、Ionic |
| 桌面应用 | Electron |
| 游戏开发 | Phaser、Three.js |
| 物联网 | Johnny-Five、Espruino |

## 学习资源

- MDN Web Docs：https://developer.mozilla.org/zh-CN/
- JavaScript.info：https://javascript.info/
- Node.js 官方文档：https://nodejs.org/
- Can I Use：https://caniuse.com/
