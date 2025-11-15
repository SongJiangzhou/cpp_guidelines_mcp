"""
C++ 编码规范 MCP 服务器

提供 C++ 代码规范检查、最佳实践建议和代码审查支持。
"""

from mcp.server.fastmcp import FastMCP

# 导入工具模块
from cpp_style.tools.naming_checker import get_checker as get_naming_checker
from cpp_style.tools.include_guard_checker import get_checker as get_include_guard_checker
from cpp_style.tools.memory_safety import get_analyzer as get_memory_analyzer
from cpp_style.tools.modern_cpp import get_suggester as get_modern_cpp_suggester
from cpp_style.tools.const_checker import get_checker as get_const_checker

# 导入资源模块
from cpp_style.resources.naming_rules import get_resource as get_naming_resource
from cpp_style.resources.best_practices import get_resource as get_practices_resource
from cpp_style.resources.cpp_standards import get_resource as get_standards_resource
from cpp_style.resources.design_patterns import get_resource as get_patterns_resource

# 创建 MCP 服务器实例
mcp = FastMCP("C++ Style Guide Server")


# ==================== Tools ====================

@mcp.tool()
def check_naming(identifier: str, category: str) -> str:
    """
    检查 C++ 标识符命名是否符合规范

    参数:
        identifier: 要检查的标识符名称
        category: 标识符类别，可选值:
                 - variable: 变量
                 - constant: 常量
                 - function: 函数
                 - class: 类
                 - namespace: 命名空间
                 - member_variable: 成员变量
                 - template_parameter: 模板参数
                 - file_naming: 文件命名

    返回:
        检查结果，包含是否符合规范、详细说明和建议
    """
    checker = get_naming_checker()
    is_valid, details, suggestions = checker.check_naming(identifier, category)

    result = details
    if suggestions:
        result += f"\n推荐使用:\n"
        for sug in suggestions:
            result += f"  • {sug}\n"

    return result


@mcp.tool()
def check_include_guard(code: str, file_path: str = "") -> str:
    """
    检查 C++ 头文件的包含保护是否正确

    参数:
        code: 头文件的完整代码
        file_path: 可选的文件路径，用于生成建议的保护宏名

    返回:
        检查结果，包含是否符合规范、详细说明和建议
    """
    checker = get_include_guard_checker()

    file_path_param = file_path if file_path else None
    is_valid, details, suggestions = checker.check_include_guard(code, file_path_param)

    result = details
    if suggestions and not is_valid:
        result += f"\n建议的保护宏名:\n"
        for sug in suggestions:
            result += f"  • {sug}\n"

    return result


@mcp.tool()
def analyze_memory_safety(code: str) -> str:
    """
    分析 C++ 代码中的内存安全问题

    参数:
        code: 要分析的 C++ 代码

    返回:
        内存安全分析报告，包括潜在的内存泄漏、悬空指针、不安全操作等
    """
    analyzer = get_memory_analyzer()
    issues, report = analyzer.analyze_memory_safety(code)
    return report


@mcp.tool()
def suggest_modern_cpp(code: str, target_standard: str = "cpp17") -> str:
    """
    建议将代码升级为现代 C++ 写法

    参数:
        code: 要分析的 C++ 代码
        target_standard: 目标 C++ 标准，可选值:
                        - cpp11: C++11
                        - cpp14: C++14
                        - cpp17: C++17 (默认)
                        - cpp20: C++20
                        - cpp23: C++23

    返回:
        现代化建议报告，包括可以使用的新特性和重写示例
    """
    suggester = get_modern_cpp_suggester()
    suggestions, report = suggester.suggest_modern_cpp(code, target_standard)
    return report


@mcp.tool()
def check_const_correctness(code: str) -> str:
    """
    检查 C++ 代码中的 const 正确性

    参数:
        code: 要检查的 C++ 代码

    返回:
        const 正确性检查报告，包括缺少 const 的地方和改进建议
    """
    checker = get_const_checker()
    issues, report = checker.check_const_correctness(code)
    return report


# ==================== Resources ====================

@mcp.resource("cpp-style://naming/{category}")
def get_naming_convention(category: str) -> str:
    """
    获取 C++ 命名规范文档

    可用的类别:
    - variable: 变量命名
    - constant: 常量命名
    - function: 函数命名
    - class: 类命名
    - namespace: 命名空间命名
    - member_variable: 成员变量命名
    - template_parameter: 模板参数命名
    - file_naming: 文件命名
    - all: 查看所有类别
    """
    resource = get_naming_resource()

    if category == "all":
        return resource.get_all_categories()

    return resource.get_naming_rule(category)


@mcp.resource("cpp-style://best-practices/{topic}")
def get_best_practice(topic: str) -> str:
    """
    获取 C++ 最佳实践指南

    可用的主题:
    - memory: 内存管理
    - exceptions: 异常处理
    - templates: 模板编程
    - concurrency: 并发编程
    - performance: 性能优化
    - modern_cpp: 现代 C++ 特性
    - all: 查看所有主题
    """
    resource = get_practices_resource()

    if topic == "all":
        return resource.get_all_topics()

    return resource.get_best_practice(topic)


@mcp.resource("cpp-style://standard/{version}")
def get_cpp_standard(version: str) -> str:
    """
    获取 C++ 标准特性文档

    可用的版本:
    - cpp11: C++11 特性
    - cpp14: C++14 特性
    - cpp17: C++17 特性
    - cpp20: C++20 特性
    - cpp23: C++23 特性
    - all: 查看所有标准概览
    """
    resource = get_standards_resource()

    if version == "all":
        return resource.get_all_standards()

    return resource.get_standard_features(version)


@mcp.resource("cpp-style://examples/{pattern}")
def get_design_pattern(pattern: str) -> str:
    """
    获取 C++ 设计模式示例

    可用的模式:
    - singleton: 单例模式
    - factory: 工厂模式
    - observer: 观察者模式
    - raii: RAII 惯用法
    - pimpl: Pimpl 惯用法
    - strategy: 策略模式
    - all: 查看所有模式
    """
    resource = get_patterns_resource()

    if pattern == "all":
        return resource.get_all_patterns()

    return resource.get_pattern_example(pattern)


# ==================== Prompts ====================

@mcp.prompt()
def code_review(focus: str = "general") -> str:
    """
    生成 C++ 代码审查提示模板

    参数:
        focus: 审查重点，可选值:
              - general: 综合审查（默认）
              - performance: 性能优化
              - safety: 内存和类型安全
              - readability: 可读性和维护性
              - modern: 现代 C++ 特性使用
    """
    base_prompt = "请对以下 C++ 代码进行审查，关注以下方面：\n\n"

    if focus == "performance":
        base_prompt += """
**性能审查重点:**
1. 是否存在不必要的拷贝？应使用引用或移动语义吗？
2. 容器使用是否合适？是否需要 reserve？
3. 算法复杂度是否最优？
4. 是否有内联优化机会？
5. 循环是否可以优化？
"""
    elif focus == "safety":
        base_prompt += """
**安全性审查重点:**
1. 是否有内存泄漏风险？
2. 是否有悬空指针或野指针？
3. 是否有数组越界风险？
4. 异常安全性如何？是否符合 RAII？
5. 是否使用了不安全的 C 风格函数？
6. 类型转换是否安全？
"""
    elif focus == "readability":
        base_prompt += """
**可读性审查重点:**
1. 命名是否清晰、符合规范？
2. 代码结构是否清晰？
3. 是否有足够的注释？
4. 函数是否过长？是否需要拆分？
5. 是否遵循单一职责原则？
"""
    elif focus == "modern":
        base_prompt += """
**现代 C++ 审查重点:**
1. 是否使用了智能指针替代裸指针？
2. 是否使用了 auto 类型推导？
3. 是否使用了范围 for 循环？
4. 是否使用了 constexpr 和 consteval？
5. 是否使用了 std::optional 和 std::variant？
6. 是否可以使用 Concepts 约束模板？
"""
    else:  # general
        base_prompt += """
**综合审查清单:**

1. **正确性**
   - 逻辑是否正确？
   - 边界条件是否处理？
   - 是否有潜在的 bug？

2. **安全性**
   - 内存管理是否安全？
   - 是否有未定义行为？
   - 异常处理是否完善？

3. **性能**
   - 是否有性能瓶颈？
   - 数据结构选择是否合理？
   - 是否有优化空间？

4. **可维护性**
   - 代码是否清晰易懂？
   - 命名是否规范？
   - 结构是否合理？

5. **现代 C++**
   - 是否充分利用现代 C++ 特性？
   - 是否遵循最佳实践？
"""

    base_prompt += "\n请提供具体的改进建议和示例代码。"

    return base_prompt


@mcp.prompt()
def refactor_suggestion(target_standard: str = "cpp17") -> str:
    """
    生成代码重构建议提示模板

    参数:
        target_standard: 目标 C++ 标准
                        - cpp11: C++11
                        - cpp14: C++14
                        - cpp17: C++17
                        - cpp20: C++20
                        - cpp23: C++23
    """
    standard_features = {
        "cpp11": [
            "auto 类型推导",
            "nullptr",
            "范围 for 循环",
            "智能指针 (unique_ptr, shared_ptr)",
            "lambda 表达式",
            "右值引用和移动语义",
        ],
        "cpp14": [
            "泛型 lambda",
            "返回值类型推导",
            "std::make_unique",
            "二进制字面量",
        ],
        "cpp17": [
            "结构化绑定",
            "if/switch 初始化语句",
            "constexpr if",
            "std::optional",
            "std::string_view",
            "折叠表达式",
        ],
        "cpp20": [
            "Concepts (概念)",
            "Ranges (区间)",
            "Coroutines (协程)",
            "三路比较运算符 (<=>)",
            "指定初始化器",
            "std::span",
        ],
        "cpp23": [
            "std::expected",
            "std::print",
            "if consteval",
            "多维下标运算符",
            "推导 this",
        ],
    }

    prompt = f"请将以下 C++ 代码重构为使用 {target_standard.upper()} 标准。\n\n"
    prompt += f"**可以使用的 {target_standard.upper()} 特性:**\n"

    # 包含目标及之前的所有标准特性
    standards = ["cpp11", "cpp14", "cpp17", "cpp20", "cpp23"]
    target_index = standards.index(target_standard)

    for std in standards[:target_index + 1]:
        if std in standard_features:
            prompt += f"\n{std.upper()} 特性:\n"
            for feature in standard_features[std]:
                prompt += f"  • {feature}\n"

    prompt += "\n**重构要求:**\n"
    prompt += "1. 使用现代 C++ 特性替代旧式写法\n"
    prompt += "2. 提高代码可读性和安全性\n"
    prompt += "3. 保持功能不变\n"
    prompt += "4. 解释每个重构点的理由\n"
    prompt += "5. 提供前后对比代码\n"

    return prompt


# 启动服务器（仅在直接运行时）
if __name__ == "__main__":
    import os

    # 从环境变量检测运行模式，默认为 stdio
    # Smithery 部署时使用 streamable-http，本地开发使用 stdio
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        # HTTP 模式：使用 uvicorn 手动启动以支持 PORT 环境变量
        import uvicorn
        port = int(os.environ.get("PORT", "8000"))

        # 获取 FastMCP 的 streamable HTTP 应用
        app = mcp.streamable_http_app

        # 启动服务器
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # stdio 模式：使用标准方式启动
        mcp.run(transport=transport)
