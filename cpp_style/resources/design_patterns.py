"""C++ 设计模式示例资源"""

import json
from pathlib import Path


class DesignPatternsResource:
    """设计模式示例资源提供器"""

    def __init__(self):
        """加载设计模式数据"""
        data_path = Path(__file__).parent.parent / "data" / "design_patterns.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            self.patterns = json.load(f)

    def get_pattern_example(self, pattern: str) -> str:
        """
        获取指定设计模式的示例

        Args:
            pattern: 模式名称 (singleton, factory, observer, raii, pimpl, strategy)

        Returns:
            格式化的设计模式文档
        """
        if pattern not in self.patterns:
            available = ', '.join(self.patterns.keys())
            return f"未知的设计模式: {pattern}\n\n可用模式: {available}"

        pat = self.patterns[pattern]

        # 构建格式化的文档
        doc = f"# {pat['name']}\n\n"
        doc += f"**分类**: {pat['category']}\n\n"
        doc += f"## 意图\n\n{pat['intent']}\n\n"

        # 适用场景
        doc += "## 适用场景\n\n"
        for use_case in pat['use_cases']:
            doc += f"- {use_case}\n"
        doc += "\n"

        # 示例代码
        doc += "## C++ 实现示例\n\n"
        if 'modern_cpp' in pat:
            doc += f"**最低要求**: {pat['modern_cpp']}\n\n"
        doc += "```cpp\n"
        doc += pat['example']
        doc += "\n```\n\n"

        # 优缺点
        if 'pros' in pat:
            doc += "## 优点\n\n"
            for pro in pat['pros']:
                doc += f"✅ {pro}\n"
            doc += "\n"

        if 'cons' in pat:
            doc += "## 缺点\n\n"
            for con in pat['cons']:
                doc += f"⚠️ {con}\n"
            doc += "\n"

        # 相关模式
        if 'alternatives' in pat:
            doc += f"## 替代方案\n\n{pat['alternatives']}\n\n"

        if 'related' in pat:
            doc += f"## 相关概念\n\n{pat['related']}\n\n"

        # 添加最佳实践
        doc += self._get_best_practices(pattern)

        return doc

    def get_all_patterns(self) -> str:
        """获取所有设计模式的概览"""
        doc = "# C++ 设计模式与惯用法\n\n"
        doc += "现代 C++ 中常用的设计模式和最佳实践\n\n"
        doc += "---\n\n"

        # 按类别分组
        by_category = {}
        for pattern_key, pattern in self.patterns.items():
            category = pattern['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((pattern_key, pattern))

        # 生成分类文档
        for category, patterns in by_category.items():
            doc += f"## {category}\n\n"
            for pattern_key, pattern in patterns:
                doc += f"### {pattern['name']}\n"
                doc += f"**意图**: {pattern['intent']}\n"
                doc += f"**资源URI**: `cpp-style://examples/{pattern_key}`\n\n"

        doc += "---\n\n"
        doc += "## 使用方式\n\n"
        doc += "使用资源 URI: `cpp-style://examples/{pattern}` 获取详细示例\n\n"
        doc += "例如:\n"
        doc += "- `cpp-style://examples/singleton` - 单例模式\n"
        doc += "- `cpp-style://examples/factory` - 工厂模式\n"
        doc += "- `cpp-style://examples/raii` - RAII 惯用法\n"

        return doc

    def _get_best_practices(self, pattern: str) -> str:
        """获取模式的最佳实践"""
        practices = {
            "singleton": """
## 💡 最佳实践

1. **使用 Meyers' Singleton**: C++11 的局部静态变量是线程安全的
2. **删除拷贝和赋值**: 使用 `= delete` 防止复制
3. **考虑替代方案**: 单例往往是全局状态，优先考虑依赖注入
4. **测试困难**: 单例会让单元测试变得困难，谨慎使用

**现代替代方案**:
```cpp
// 使用依赖注入替代单例
class Logger { /* ... */ };

class App {
public:
    App(Logger& logger) : logger_(logger) {}
private:
    Logger& logger_;  // 注入依赖
};
```
""",
            "factory": """
## 💡 最佳实践

1. **使用智能指针**: 工厂返回 `std::unique_ptr` 或 `std::shared_ptr`
2. **考虑使用 enum class**: 类型安全的产品类型标识
3. **C++17 可选**: 返回 `std::optional` 处理创建失败
4. **注册机制**: 对于插件系统，使用注册表自动注册工厂

**现代写法**:
```cpp
std::optional<std::unique_ptr<Shape>> createShape(ShapeType type) {
    // 返回 optional 表示可能失败
}
```
""",
            "observer": """
## 💡 最佳实践

1. **使用 weak_ptr**: 避免循环引用导致的内存泄漏
2. **线程安全**: 多线程环境下保护观察者列表
3. **C++20 考虑**: 可以使用 `std::function` 或信号槽库
4. **现代替代**: 考虑使用 RxCpp (Reactive Extensions)

**信号槽风格**:
```cpp
// 使用 std::function 实现简单的信号槽
using Slot = std::function<void(const Event&)>;
std::vector<Slot> slots_;
```
""",
            "raii": """
## 💡 最佳实践

1. **遵循规则**: 资源在构造函数中获取，析构函数中释放
2. **移动语义**: 使用移动构造和移动赋值转移所有权
3. **删除拷贝**: 大多数情况下应禁止拷贝
4. **标准库示例**: 学习 `std::unique_ptr`, `std::lock_guard` 的实现

**遵循五法则或零法则**:
```cpp
class Resource {
public:
    ~Resource();                                    // 析构
    Resource(Resource&&) noexcept;                  // 移动构造
    Resource& operator=(Resource&&) noexcept;       // 移动赋值
    Resource(const Resource&) = delete;             // 禁止拷贝
    Resource& operator=(const Resource&) = delete;  // 禁止拷贝赋值
};
```
""",
            "pimpl": """
## 💡 最佳实践

1. **unique_ptr**: 使用 `std::unique_ptr<Impl>` 而非裸指针
2. **析构函数**: 必须在 .cpp 中定义，否则 unique_ptr 无法删除不完整类型
3. **移动语义**: 实现移动构造和移动赋值
4. **性能考虑**: 有间接调用开销，权衡编译时间和运行时性能

**完整实现要点**:
```cpp
// .h
class Widget {
    ~Widget();  // 必须在 .cpp 中定义
    Widget(Widget&&) noexcept;  // = default 在 .cpp 中
    // ...
};
```
""",
            "strategy": """
## 💡 最佳实践

1. **模板策略**: 编译期策略可以使用模板参数
2. **std::function**: 简单策略可以直接使用函数对象
3. **lambda 表达式**: C++11 lambda 可以作为轻量级策略
4. **性能**: 虚函数有开销，性能敏感代码考虑模板

**使用 std::function 的轻量级版本**:
```cpp
class Compressor {
public:
    using Strategy = std::function<std::vector<uint8_t>(const std::vector<uint8_t>&)>;

    void setStrategy(Strategy strategy) {
        strategy_ = std::move(strategy);
    }
private:
    Strategy strategy_;
};

// 使用 lambda
compressor.setStrategy([](const auto& data) {
    return zipCompress(data);
});
```
"""
        }

        return practices.get(pattern, "")


# 全局实例
_resource = None

def get_resource() -> DesignPatternsResource:
    """获取全局资源实例"""
    global _resource
    if _resource is None:
        _resource = DesignPatternsResource()
    return _resource
