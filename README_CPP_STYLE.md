# C++ 编码规范 MCP 服务器

一个基于 Model Context Protocol (MCP) 的 C++ 编码规范服务器，提供代码规范检查、最佳实践建议和代码审查支持。

## 📋 功能特性

### 🛠️ Tools（工具） - 5个强大功能

#### 1. `check_naming` - 命名规范检查
检查 C++ 标识符命名是否符合规范。

**参数:**
- `identifier` (string): 要检查的标识符名称
- `category` (string): 标识符类别
  - `variable`: 变量
  - `constant`: 常量
  - `function`: 函数
  - `class`: 类
  - `namespace`: 命名空间
  - `member_variable`: 成员变量
  - `template_parameter`: 模板参数
  - `file_naming`: 文件命名

**示例:**
```python
check_naming("userName", "variable")
# 返回: 不符合规范，建议使用 user_name

check_naming("MAX_SIZE", "constant")
# 返回: 符合规范
```

#### 2. `check_include_guard` - 包含保护检查
检查 C++ 头文件的包含保护是否正确。

**参数:**
- `code` (string): 头文件的完整代码
- `file_path` (string, 可选): 文件路径，用于生成建议的保护宏名

**示例:**
```python
check_include_guard("""
#pragma once

class MyClass {
    // ...
};
""", "myclass.h")
# 返回: 符合规范（使用了 #pragma once）

check_include_guard("""
#ifndef MYCLASS_H
#define MYCLASS_H

class MyClass {
    // ...
};

#endif
""", "myclass.h")
# 返回: 符合规范（使用了传统保护）
```

#### 3. `analyze_memory_safety` - 内存安全分析 ⭐新增
分析代码中的内存安全问题。

**参数:**
- `code` (string): 要分析的 C++ 代码

**检测内容:**
- 裸指针使用 (new/delete)
- 手动内存管理
- C 风格内存函数 (malloc/free)
- 不安全的字符串操作 (strcpy/strcat)
- 潜在的内存泄漏
- 悬空指针风险
- 数组访问安全

**示例:**
```python
analyze_memory_safety("""
Widget* w = new Widget();
// ... 使用 w
delete w;
""")
# 返回: 建议使用智能指针
```

#### 4. `suggest_modern_cpp` - 现代 C++ 建议 ⭐新增
建议将代码升级为现代 C++ 写法。

**参数:**
- `code` (string): 要分析的 C++ 代码
- `target_standard` (string): 目标标准 (cpp11/cpp14/cpp17/cpp20/cpp23)，默认 cpp17

**提供建议:**
- C++11: auto, nullptr, 智能指针, 范围for, lambda等
- C++14: make_unique, 泛型lambda, 返回值推导
- C++17: 结构化绑定, if初始化, optional, string_view
- C++20: Concepts, Ranges, 三路比较, span
- C++23: expected, print, if consteval

**示例:**
```python
suggest_modern_cpp("""
int* ptr = NULL;
typedef std::vector<int> IntVec;
for (auto it = vec.begin(); it != vec.end(); ++it) {
    process(*it);
}
""", "cpp17")
# 返回: 建议使用 nullptr, using, 范围for等
```

#### 5. `check_const_correctness` - const 正确性检查 ⭐新增
检查代码中的 const 使用是否正确。

**参数:**
- `code` (string): 要检查的 C++ 代码

**检查内容:**
- 成员函数是否应该是 const
- 函数参数是否应该使用 const 引用
- 返回值是否应该是 const
- 局部变量是否应该是 const
- 指针/引用的 const 正确性

**示例:**
```python
check_const_correctness("""
class MyClass {
    int getValue() { return value_; }
    void process(std::string str) { ... }
};
""")
# 返回: getValue() 应该是 const, str 应该是 const&
```

### 📚 Resources（资源） - 4类丰富内容

#### 1. `cpp-style://naming/{category}` - 命名规范文档
获取指定类别的详细命名规范。

**可用类别:**
- `variable` - 变量命名规范
- `constant` - 常量命名规范
- `function` - 函数命名规范
- `class` - 类命名规范
- `namespace` - 命名空间命名规范
- `member_variable` - 成员变量命名规范
- `template_parameter` - 模板参数命名规范
- `file_naming` - 文件命名规范
- `all` - 查看所有类别概览

**示例:**
```
cpp-style://naming/variable
cpp-style://naming/class
cpp-style://naming/all
```

#### 2. `cpp-style://best-practices/{topic}` - 最佳实践指南
获取指定主题的详细最佳实践。

**可用主题:**
- `memory` - 内存管理最佳实践
- `exceptions` - 异常处理最佳实践
- `templates` - 模板编程最佳实践
- `concurrency` - 并发编程最佳实践
- `performance` - 性能优化最佳实践
- `modern_cpp` - 现代 C++ 特性使用
- `all` - 查看所有主题概览

**示例:**
```
cpp-style://best-practices/memory
cpp-style://best-practices/modern_cpp
cpp-style://best-practices/all
```

#### 3. `cpp-style://standard/{version}` - C++ 标准特性 ⭐新增
获取指定 C++ 标准的详细特性说明。

**可用版本:**
- `cpp11` - C++11 特性
- `cpp14` - C++14 特性
- `cpp17` - C++17 特性
- `cpp20` - C++20 特性
- `cpp23` - C++23 特性
- `all` - 查看所有标准概览

**内容包含:**
- 每个特性的详细说明
- 完整的代码示例
- 使用建议和最佳实践
- 学习资源链接

**示例:**
```
cpp-style://standard/cpp17
cpp-style://standard/cpp20
cpp-style://standard/all
```

#### 4. `cpp-style://examples/{pattern}` - 设计模式示例 ⭐新增
获取 C++ 设计模式的完整实现示例。

**可用模式:**
- `singleton` - 单例模式（线程安全的 Meyers' Singleton）
- `factory` - 工厂模式（使用智能指针）
- `observer` - 观察者模式（使用 weak_ptr 避免循环引用）
- `raii` - RAII 惯用法（资源管理）
- `pimpl` - Pimpl 惯用法（隐藏实现）
- `strategy` - 策略模式（算法替换）
- `all` - 查看所有模式概览

**内容包含:**
- 模式意图和适用场景
- 现代 C++ 实现（C++11+）
- 完整可运行的代码
- 优缺点分析
- 最佳实践建议

**示例:**
```
cpp-style://examples/singleton
cpp-style://examples/raii
cpp-style://examples/all
```

### 💡 Prompts（提示模板）

#### 1. `code_review` - 代码审查提示
生成 C++ 代码审查提示模板。

**参数:**
- `focus` (string, 可选): 审查重点
  - `general`: 综合审查（默认）
  - `performance`: 性能优化
  - `safety`: 内存和类型安全
  - `readability`: 可读性和维护性
  - `modern`: 现代 C++ 特性使用

**示例:**
```python
code_review(focus="performance")
code_review(focus="safety")
```

#### 2. `refactor_suggestion` - 重构建议提示
生成代码重构建议提示模板。

**参数:**
- `target_standard` (string, 可选): 目标 C++ 标准
  - `cpp11`: C++11（默认）
  - `cpp14`: C++14
  - `cpp17`: C++17
  - `cpp20`: C++20
  - `cpp23`: C++23

**示例:**
```python
refactor_suggestion(target_standard="cpp20")
```

## 🚀 快速开始

### 本地运行（stdio 模式）

```bash
uv run mcp run cpp_style_server.py
```

### 网络模式（SSE 传输）

```bash
# 本地开发
uv run mcp run cpp_style_server.py --transport sse --port 8000

# 允许外部访问
uv run mcp run cpp_style_server.py --transport sse --host 0.0.0.0 --port 8000
```

### 在 Claude Code 中安装

#### 本地安装（stdio 模式）

```bash
claude mcp add --transport stdio cpp-style -- uv run mcp run cpp_style_server.py
```

#### 网络模式（连接远程服务器）

```bash
claude mcp add --transport sse cpp-style http://localhost:8000/sse
```

### 验证安装

```bash
claude mcp list
```

或在 Claude Code 对话中使用:
```
/mcp
```

## 📖 使用示例

### 1. 检查变量命名

在 Claude Code 中，服务器会自动调用工具：

```
请检查这个变量名是否符合 C++ 规范：userName
```

Claude 会自动调用 `check_naming` 工具并返回建议。

### 2. 检查头文件包含保护

```
请检查这个头文件的包含保护是否正确：
[粘贴你的头文件代码]
```

### 3. 查看最佳实践

```
请告诉我 C++ 内存管理的最佳实践
```

Claude 会访问 `cpp-style://best-practices/memory` 资源。

### 4. 代码审查

```
请对以下代码进行性能审查：
[粘贴你的代码]
```

Claude 会使用 `code_review` 提示模板进行审查。

## 🏗️ 项目结构

```
cpp_style/
├── __init__.py
├── tools/                          # 工具模块
│   ├── __init__.py
│   ├── naming_checker.py           # 命名检查工具
│   └── include_guard_checker.py    # 包含保护检查工具
├── resources/                      # 资源模块
│   ├── __init__.py
│   ├── naming_rules.py             # 命名规范资源
│   └── best_practices.py           # 最佳实践资源
├── prompts/                        # 提示模板（预留）
│   └── __init__.py
└── data/                           # 规范数据
    ├── naming_conventions.json     # 命名规范数据
    ├── best_practices.json         # 最佳实践数据
    └── cpp_standards.json          # C++ 标准特性数据
```

## 📝 支持的命名规范

### 变量 (variable)
- **风格**: `snake_case`
- **示例**: `user_name`, `total_count`, `max_value`

### 常量 (constant)
- **风格**: `UPPER_SNAKE_CASE` 或 `kCamelCase`
- **示例**: `MAX_BUFFER_SIZE`, `kDefaultTimeout`

### 函数 (function)
- **风格**: `snake_case` 或 `CamelCase`
- **示例**: `calculate_total`, `CalculateTotal`

### 类 (class)
- **风格**: `PascalCase`
- **示例**: `UserManager`, `HttpClient`

### 命名空间 (namespace)
- **风格**: `snake_case` 或 `lowercase`
- **示例**: `utils`, `http_client`

### 成员变量 (member_variable)
- **风格**: 下划线后缀或 `m_` 前缀
- **示例**: `name_`, `m_name`

### 模板参数 (template_parameter)
- **风格**: `PascalCase` 或单个大写字母
- **示例**: `T`, `TKey`, `Container`

## 🎯 最佳实践主题

1. **内存管理** (`memory`)
   - 智能指针使用
   - RAII 原则
   - 内存泄漏预防
   - 悬空指针避免

2. **异常处理** (`exceptions`)
   - 按引用捕获异常
   - 析构函数中的异常
   - 自定义异常类型

3. **模板编程** (`templates`)
   - typename vs class
   - Concepts 使用
   - 模板代码膨胀

4. **并发编程** (`concurrency`)
   - 标准库工具
   - 死锁避免
   - 原子操作
   - async 和 futures

5. **性能优化** (`performance`)
   - 引用传递
   - 移动语义
   - 容器预分配
   - Profiling

6. **现代 C++** (`modern_cpp`)
   - auto 类型推导
   - 范围 for 循环
   - nullptr
   - override 和 final
   - constexpr

## 🔧 扩展和定制

### 添加新的命名类别

编辑 `cpp_style/data/naming_conventions.json`:

```json
{
  "new_category": {
    "style": "your_style",
    "description": "描述",
    "examples": {
      "good": ["example1"],
      "bad": ["example2"]
    },
    "rules": ["规则1", "规则2"]
  }
}
```

### 添加新的最佳实践

编辑 `cpp_style/data/best_practices.json`:

```json
{
  "new_topic": {
    "title": "标题",
    "rules": [
      {
        "name": "规则名称",
        "description": "描述",
        "good_example": "// 正确代码",
        "bad_example": "// 错误代码",
        "reason": "原因"
      }
    ]
  }
}
```

### 添加新的工具

在 `cpp_style_server.py` 中:

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    """工具描述"""
    # 实现逻辑
    return result
```

## 📚 参考资源

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html)
- [cppreference.com](https://en.cppreference.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请在 GitHub 上提 Issue。

---

## 🆕 版本更新

### 阶段2+ - 功能完善版 (当前版本)

新增内容：

**新增工具 (阶段2)**:
- ✅ **内存安全分析** - 检测内存泄漏、悬空指针、不安全操作
- ✅ **现代 C++ 建议** - 支持 C++11~C++23，提供现代化重写建议
- ✅ **const 正确性检查** - 全面检查 const 使用

**新增资源 (阶段2+)**:
- ✅ **C++ 标准特性** - C++11 到 C++23 的完整特性文档
- ✅ **设计模式示例** - 6种常用模式的现代 C++ 实现

**当前状态总览**:
- **工具总数**: 5个
  - check_naming (命名规范检查)
  - check_include_guard (包含保护检查)
  - analyze_memory_safety (内存安全分析)
  - suggest_modern_cpp (现代 C++ 建议)
  - check_const_correctness (const 正确性检查)

- **资源总数**: 4类
  - cpp-style://naming/{category} (8类命名规范)
  - cpp-style://best-practices/{topic} (6大主题最佳实践)
  - cpp-style://standard/{version} (C++11~23 标准特性) ⭐新增
  - cpp-style://examples/{pattern} (6种设计模式) ⭐新增

- **提示模板**: 2个
  - code_review (代码审查提示)
  - refactor_suggestion (重构建议提示)

### 阶段1 - 基础实现

包含核心的命名规范检查和包含保护检查功能。
