# TypeScript 语言详解

## 简介

TypeScript 是由 Microsoft 开发和维护的开源编程语言，是 JavaScript 的超集，添加了可选的静态类型和基于类的面向对象编程。TypeScript 编译为纯 JavaScript，可在任何支持 JS 的环境中运行。

## 核心特点

- **静态类型**：编译时类型检查，提前发现错误
- **类型推断**：自动推断变量类型
- **接口和类型**：强大的类型系统
- **泛型**：编写可复用的类型安全代码
- **装饰器**：AOP 编程支持
- **完全兼容**：所有合法的 JS 代码都是合法的 TS 代码

## 语法示例

### 基础类型

```typescript
// 基本类型
let name: string = "TypeScript";
let version: number = 5.3;
let isAwesome: boolean = true;

// 数组
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["Alice", "Bob"];

// 元组
let person: [string, number] = ["Alice", 30];

// 枚举
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}
let dir: Direction = Direction.Up;

// 特殊类型
let anything: any = "可以是任何类型";
let unknown: unknown = "类型安全的 any";
let nothing: void = undefined;
let never: never;  // 永远不会有值

// 类型别名
type ID = string | number;
type Point = { x: number; y: number };

// 接口
interface User {
    id: ID;
    name: string;
    email?: string;  // 可选属性
    readonly createdAt: Date;  // 只读属性
}
```

### 函数

```typescript
// 函数类型
function add(a: number, b: number): number {
    return a + b;
}

// 箭头函数
const multiply = (a: number, b: number): number => a * b;

// 可选参数和默认值
function greet(name: string, greeting: string = "Hello"): string {
    return `${greeting}, ${name}!`;
}

// 剩余参数
function sum(...numbers: number[]): number {
    return numbers.reduce((acc, n) => acc + n, 0);
}

// 函数重载
function parse(input: string): string;
function parse(input: number): string;
function parse(input: string | number): string {
    if (typeof input === "string") {
        return input.toUpperCase();
    }
    return input.toString();
}

// 泛型函数
function identity<T>(arg: T): T {
    return arg;
}

function getFirst<T>(arr: T[]): T | undefined {
    return arr[0];
}

// 使用
const num = identity<number>(42);
const str = identity("hello");
const first = getFirst([1, 2, 3]);
```

### 类和面向对象

```typescript
// 接口
interface Shape {
    area(): number;
    perimeter(): number;
}

// 抽象类
abstract class Animal {
    constructor(protected name: string, protected sound: string) {}
    
    abstract speak(): string;
    
    describe(): string {
        return `${this.name} makes ${this.sound}`;
    }
}

// 类实现接口
class Circle implements Shape {
    constructor(private radius: number) {}
    
    area(): number {
        return Math.PI * this.radius ** 2;
    }
    
    perimeter(): number {
        return 2 * Math.PI * this.radius;
    }
}

// 继承
class Dog extends Animal {
    constructor(name: string) {
        super(name, "Woof");
    }
    
    speak(): string {
        return `${this.name} says ${this.sound}!`;
    }
    
    fetch(item: string): string {
        return `${this.name} fetches the ${item}`;
    }
}

// 访问修饰符
class User {
    public name: string;
    private password: string;
    protected email: string;
    readonly id: number;
    
    constructor(name: string, password: string, email: string) {
        this.id = Date.now();
        this.name = name;
        this.password = password;
        this.email = email;
    }
}

// 使用
const circle = new Circle(5);
console.log(`面积: ${circle.area()}`);

const dog = new Dog("Buddy");
console.log(dog.speak());
```

### 泛型

```typescript
// 泛型接口
interface Repository<T> {
    getById(id: number): T | null;
    getAll(): T[];
    save(item: T): void;
    delete(id: number): boolean;
}

// 泛型类
class InMemoryRepository<T extends { id: number }> implements Repository<T> {
    private items: T[] = [];
    
    getById(id: number): T | null {
        return this.items.find(item => item.id === id) || null;
    }
    
    getAll(): T[] {
        return [...this.items];
    }
    
    save(item: T): void {
        const index = this.items.findIndex(i => i.id === item.id);
        if (index >= 0) {
            this.items[index] = item;
        } else {
            this.items.push(item);
        }
    }
    
    delete(id: number): boolean {
        const index = this.items.findIndex(item => item.id === id);
        if (index >= 0) {
            this.items.splice(index, 1);
            return true;
        }
        return false;
    }
}

// 泛型约束
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

// 条件类型
type IsString<T> = T extends string ? true : false;
type A = IsString<string>;  // true
type B = IsString<number>;  // false
```

### 高级类型

```typescript
// 联合类型
type Status = "pending" | "active" | "completed";
type NumberOrString = number | string;

// 交叉类型
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;

// 映射类型
type Optional<T> = {
    [K in keyof T]?: T[K];
};

type Readonly<T> = {
    readonly [K in keyof T]: T[K];
};

// 条件类型
type Extract<T> = T extends Array<infer U> ? U : never;

// 模板字面量类型
type EventName = `on${Capitalize<"click" | "hover">}`;
// 结果: "onClick" | "onHover"

// 类型守卫
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function process(value: string | number) {
    if (isString(value)) {
        console.log(value.toUpperCase());
    } else {
        console.log(value.toFixed(2));
    }
}

// 使用
type UserWithOptionalEmail = Optional<{ name: string; email: string }>;
type ReadonlyUser = Readonly<{ name: string; age: number }>;
```

## 优缺点

### 优点

- ✅ 提前发现类型错误
- ✅ 更好的 IDE 支持（自动补全、重构）
- ✅ 代码更易读和维护
- ✅ 渐进式采用，不破坏现有 JS 代码
- ✅ 强大的类型系统
- ✅ 优秀的工具链

### 缺点

- ❌ 额外的编译步骤
- ❌ 类型定义可能很复杂
- ❌ 学习曲线较陡
- ❌ 某些 JS 库的类型定义不完善
- ❌ 编译后代码体积可能增大

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| 前端开发 | React、Vue、Angular 项目 |
| 后端开发 | Node.js、NestJS |
| 全栈应用 | Next.js、Nuxt.js |
| 库开发 | 编写类型安全的库 |
| 大型项目 | 需要长期维护的项目 |
| 团队协作 | 提高代码一致性 |

## 学习资源

- TypeScript 官方文档：https://www.typescriptlang.org/
- TypeScript Playground：https://www.typescriptlang.org/play
- TypeScript Deep Dive：https://basarat.gitbook.io/typescript
- Matt Pocock 的教程：https://www.totaltypescript.com/
