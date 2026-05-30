# PHP 语言详解

## 简介

PHP（Hypertext Preprocessor）是一种通用的脚本语言，特别适合 Web 开发。由 Rasmus Lerdorf 于 1994 年创建，PHP 可以嵌入 HTML 中执行，是服务器端脚本语言的先驱之一。目前 PHP 驱动着全球超过 77% 的网站。

## 核心特点

- **Web 原生**：专为 Web 开发设计
- **嵌入式**：可直接嵌入 HTML 中
- **跨平台**：支持各种操作系统和 Web 服务器
- **丰富的框架**：Laravel、Symfony、CodeIgniter 等
- **数据库支持**：原生支持多种数据库
- **社区庞大**：拥有海量的文档和资源

## 语法示例

### 基础语法

```php
<?php
// 变量（以 $ 开头）
$name = "PHP";
$version = 8.3;
$is_awesome = true;
$languages = ["PHP", "Python", "JavaScript"];

// 常量
define('APP_NAME', 'My App');
const MAX_SIZE = 100;

// 数组
$fruits = ["apple", "banana", "orange"];
$person = [
    "name" => "Alice",
    "age" => 30,
    "city" => "Beijing"
];

// 条件语句
if ($version >= 8.3) {
    echo "最新版本";
} elseif ($version >= 8.0) {
    echo "现代版本";
} else {
    echo "旧版本";
}

// 循环
foreach ($fruits as $fruit) {
    echo $fruit . "\n";
}

// for 循环
for ($i = 0; $i < count($fruits); $i++) {
    echo $fruits[$i] . "\n";
}

// while 循环
$i = 0;
while ($i < 5) {
    echo $i . "\n";
    $i++;
}
?>
```

### 函数

```php
<?php
// 基础函数
function add(int $a, int $b): int {
    return $a + $b;
}

// 默认参数
function greet(string $name, string $greeting = "Hello"): string {
    return "$greeting, $name!";
}

// 可变参数
function sum(int ...$numbers): int {
    return array_sum($numbers);
}

// 返回类型
function divide(float $a, float $b): array {
    if ($b == 0) {
        return ["error" => "除数不能为零"];
    }
    return ["result" => $a / $b];
}

// 匿名函数
$multiply = function(int $a, int $b): int {
    return $a * $b;
};

// 箭头函数（PHP 7.4+）
$square = fn(int $n): int => $n * $n;

// 使用
echo add(3, 4);        // 7
echo greet("World");   // Hello, World!
echo sum(1, 2, 3, 4);  // 10
echo $multiply(3, 4);  // 12
echo $square(5);       // 25
?>
```

### 类和面向对象

```php
<?php
// 接口
interface Shape {
    public function area(): float;
    public function perimeter(): float;
}

// 抽象类
abstract class Animal {
    public function __construct(
        protected string $name,
        protected string $sound
    ) {}
    
    abstract public function speak(): string;
    
    public function describe(): string {
        return "{$this->name} makes {$this->sound}";
    }
}

// 类实现接口
class Circle implements Shape {
    public function __construct(
        private float $radius
    ) {}
    
    public function area(): float {
        return M_PI * $this->radius ** 2;
    }
    
    public function perimeter(): float {
        return 2 * M_PI * $this->radius;
    }
}

// 继承
class Dog extends Animal {
    public function __construct(string $name) {
        parent::__construct($name, "Woof");
    }
    
    public function speak(): string {
        return "{$this->name} says {$this->sound}!";
    }
    
    public function fetch(string $item): string {
        return "{$this->name} fetches the $item";
    }
}

// 使用
$circle = new Circle(5);
echo "面积: " . $circle->area() . "\n";

$dog = new Dog("Buddy");
echo $dog->speak() . "\n";
echo $dog->fetch("ball") . "\n";
?>
```

### 错误处理

```php
<?php
// 异常处理
class InvalidArgumentException extends Exception {}

function setAge(int $age): void {
    if ($age < 0 || $age > 150) {
        throw new InvalidArgumentException("年龄无效: $age");
    }
    echo "年龄设置为: $age\n";
}

try {
    setAge(25);
    setAge(-5);
} catch (InvalidArgumentException $e) {
    echo "错误: " . $e->getMessage() . "\n";
} finally {
    echo "执行完成\n";
}

// PHP 8+ 的 Match 表达式
$status = 200;
$message = match($status) {
    200 => "成功",
    301 => "重定向",
    404 => "未找到",
    500 => "服务器错误",
    default => "未知状态"
};
echo $message . "\n";

// Null 安全运算符（PHP 8+）
$user = null;
echo $user?->name ?? "匿名用户";  // 匿名用户
?>
```

### 命名空间和自动加载

```php
<?php
// 命名空间
namespace App\Models;

use App\Database\Connection;

class User {
    public function __construct(
        private Connection $db
    ) {}
    
    public function find(int $id): ?array {
        return $this->db->query("SELECT * FROM users WHERE id = ?", [$id]);
    }
}

// PSR-4 自动加载
spl_autoload_register(function (string $class) {
    $prefix = "App\\";
    $baseDir = __DIR__ . "/src/";
    
    $relativeClass = substr($class, strlen($prefix));
    $file = $baseDir . str_replace("\\", "/", $relativeClass) . ".php";
    
    if (file_exists($file)) {
        require $file;
    }
});
?>
```

## 优缺点

### 优点

- ✅ Web 开发的首选语言
- ✅ 学习曲线平缓
- ✅ 部署简单（几乎所有主机都支持）
- ✅ 丰富的框架和 CMS（WordPress、Laravel）
- ✅ 性能优秀（PHP 8+ JIT 编译）
- ✅ 庞大的社区和文档

### 缺点

- ❌ 历史遗留问题（旧版本质量参差不齐）
- ❌ 类型系统较弱（PHP 7+ 改善很多）
- ❌ 不适合非 Web 应用
- ❌ 安全问题需要注意
- ❌ 异步编程支持有限

## 适用场景

| 领域 | 具体应用 |
|------|----------|
| Web 开发 | 动态网站、Web 应用 |
| CMS | WordPress、Drupal、Joomla |
| 电商平台 | WooCommerce、Magento |
| 后端 API | RESTful API、GraphQL |
| 微服务 | Laravel Microservices |
| 命令行工具 | Laravel Artisan、WP-CLI |

## 学习资源

- PHP 官方文档：https://www.php.net/
- PHP The Right Way：https://phptherightway.com/
- Laravel 文档：https://laravel.com/docs
- PHP 8 新特性：https://www.php.net/releases/8.3/en.php
