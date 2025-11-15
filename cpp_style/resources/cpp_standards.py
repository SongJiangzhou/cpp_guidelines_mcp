"""C++ 标准特性资源"""

import json
from pathlib import Path


class CppStandardsResource:
    """C++ 标准特性资源提供器"""

    def __init__(self):
        """加载 C++ 标准特性数据"""
        data_path = Path(__file__).parent.parent / "data" / "cpp_standards.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            self.standards = json.load(f)

    def get_standard_features(self, version: str) -> str:
        """
        获取指定 C++ 标准的特性说明

        Args:
            version: 版本名称 (cpp11, cpp14, cpp17, cpp20, cpp23)

        Returns:
            格式化的标准特性文档
        """
        if version not in self.standards:
            available = ', '.join(self.standards.keys())
            return f"未知的 C++ 标准版本: {version}\n\n可用版本: {available}"

        standard = self.standards[version]

        # 构建格式化的文档
        doc = f"# {standard['title']}\n\n"
        doc += "---\n\n"

        for feature in standard['features']:
            doc += f"## {feature['name']}\n\n"
            doc += f"{feature['description']}\n\n"

            doc += "**示例代码:**\n"
            doc += "```cpp\n"
            doc += feature['example']
            doc += "\n```\n\n"

            doc += "---\n\n"

        # 添加总结和资源
        doc += self._get_summary(version)

        return doc

    def get_all_standards(self) -> str:
        """获取所有 C++ 标准的概览"""
        doc = "# C++ 标准特性演进\n\n"
        doc += "从 C++11 到 C++23 的主要特性概览\n\n"
        doc += "---\n\n"

        for version in ['cpp11', 'cpp14', 'cpp17', 'cpp20', 'cpp23']:
            if version in self.standards:
                standard = self.standards[version]
                doc += f"## {standard['title']}\n\n"
                doc += f"**特性数量**: {len(standard['features'])}\n\n"
                doc += "**主要特性**:\n"

                # 列出前5个特性
                for i, feature in enumerate(standard['features'][:5], 1):
                    doc += f"{i}. **{feature['name']}**: {feature['description']}\n"

                if len(standard['features']) > 5:
                    doc += f"... 还有 {len(standard['features']) - 5} 个特性\n"

                doc += "\n"

        doc += "---\n\n"
        doc += "## 使用方式\n\n"
        doc += "使用资源 URI: `cpp-style://standard/{version}` 获取详细特性说明\n\n"
        doc += "例如:\n"
        doc += "- `cpp-style://standard/cpp11` - C++11 特性\n"
        doc += "- `cpp-style://standard/cpp17` - C++17 特性\n"
        doc += "- `cpp-style://standard/cpp20` - C++20 特性\n"

        return doc

    def _get_summary(self, version: str) -> str:
        """获取版本总结"""
        summaries = {
            "cpp11": """
## 💡 C++11 总结

C++11 是现代 C++ 的开端，带来了革命性的变化：

**核心改进:**
- 更好的内存管理（智能指针）
- 更简洁的语法（auto, 范围for, lambda）
- 更强的类型安全（nullptr, enum class）
- 并发支持（std::thread, std::mutex）
- 移动语义提升性能

**学习资源:**
- [C++11 FAQ](https://isocpp.org/wiki/faq/cpp11)
- [cppreference C++11](https://en.cppreference.com/w/cpp/11)
""",
            "cpp14": """
## 💡 C++14 总结

C++14 是 C++11 的完善和增强：

**主要改进:**
- 更灵活的类型推导
- 更强大的 lambda 表达式
- make_unique 补全智能指针工厂函数
- 更好的 constexpr 支持

**升级建议:**
如果使用 C++11，强烈建议升级到 C++14，几乎没有兼容性问题。

**学习资源:**
- [C++14 Overview](https://isocpp.org/wiki/faq/cpp14)
""",
            "cpp17": """
## 💡 C++17 总结

C++17 带来了大量实用特性：

**核心特性:**
- 结构化绑定简化代码
- std::optional 和 std::variant 增强类型安全
- std::string_view 提升性能
- if constexpr 优化模板代码
- 文件系统库

**适用场景:**
C++17 是目前最推荐的生产环境标准，兼顾了现代性和稳定性。

**学习资源:**
- [C++17 Features](https://en.cppreference.com/w/cpp/17)
- [C++17 in Detail](https://leanpub.com/cpp17)
""",
            "cpp20": """
## 💡 C++20 总结

C++20 是自 C++11 以来最大的更新：

**革命性特性:**
- **Concepts**: 约束模板参数，提供清晰的错误信息
- **Ranges**: 函数式编程风格的容器操作
- **Coroutines**: 协程支持异步编程
- **Modules**: 替代头文件系统
- **三路比较**: 简化比较运算符实现

**采用建议:**
编译器支持逐渐成熟，可以在新项目中谨慎使用。

**学习资源:**
- [C++20 Overview](https://en.cppreference.com/w/cpp/20)
- [C++20 The Big Four](https://www.modernescpp.com/index.php/c-20-the-big-four)
""",
            "cpp23": """
## 💡 C++23 总结

C++23 继续完善现代 C++：

**重要特性:**
- std::expected 改善错误处理
- std::print 简化输出
- std::mdspan 多维数组视图
- 更多的 constexpr 支持

**状态:**
标准已发布，编译器支持正在推进中。

**学习资源:**
- [C++23 Features](https://en.cppreference.com/w/cpp/23)
"""
        }

        return summaries.get(version, "")


# 全局实例
_resource = None

def get_resource() -> CppStandardsResource:
    """获取全局资源实例"""
    global _resource
    if _resource is None:
        _resource = CppStandardsResource()
    return _resource
