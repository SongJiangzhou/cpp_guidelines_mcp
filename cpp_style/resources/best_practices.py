"""C++ 最佳实践资源"""

import json
from pathlib import Path
from typing import Optional


class BestPracticesResource:
    """最佳实践资源提供器"""

    def __init__(self):
        """加载最佳实践数据"""
        data_path = Path(__file__).parent.parent / "data" / "best_practices.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            self.practices = json.load(f)

    def get_best_practice(self, topic: str) -> str:
        """
        获取指定主题的最佳实践

        Args:
            topic: 主题名称 (memory, exceptions, templates, concurrency, performance, modern_cpp)

        Returns:
            格式化的最佳实践文档
        """
        if topic not in self.practices:
            available = ', '.join(self.practices.keys())
            return f"未知的主题: {topic}\n\n可用主题: {available}"

        practice = self.practices[topic]

        # 构建格式化的文档
        doc = f"# {practice['title']}\n\n"

        for rule in practice['rules']:
            doc += f"## {rule['name']}\n\n"

            # 描述
            if 'description' in rule:
                doc += f"{rule['description']}\n\n"

            # 正确示例
            if 'good_example' in rule:
                doc += "**正确做法:**\n"
                doc += "```cpp\n"
                doc += rule['good_example']
                doc += "\n```\n\n"

            # 错误示例
            if 'bad_example' in rule:
                doc += "**错误做法:**\n"
                doc += "```cpp\n"
                doc += rule['bad_example']
                doc += "\n```\n\n"

            # 原因
            if 'reason' in rule:
                doc += f"**原因:** {rule['reason']}\n\n"

            # 提示
            if 'tips' in rule:
                doc += "**提示:**\n"
                for tip in rule['tips']:
                    doc += f"- {tip}\n"
                doc += "\n"

            doc += "---\n\n"

        # 添加相关资源
        doc += self._get_related_resources(topic)

        return doc

    def get_all_topics(self) -> str:
        """获取所有可用主题的概览"""
        doc = "# C++ 最佳实践主题\n\n"
        doc += "以下是所有可用的最佳实践主题：\n\n"

        for topic, practice in self.practices.items():
            doc += f"## {topic}\n"
            doc += f"**标题**: {practice['title']}\n"
            doc += f"**规则数量**: {len(practice['rules'])}\n"
            doc += f"**主要内容**: "

            # 列出前3个规则名称
            rule_names = [rule['name'] for rule in practice['rules'][:3]]
            doc += ", ".join(rule_names)
            if len(practice['rules']) > 3:
                doc += f", 等 {len(practice['rules'])} 条规则"
            doc += "\n\n"

        doc += "\n## 使用方式\n"
        doc += "使用资源 URI: `cpp-style://best-practices/{topic}` 获取详细内容\n"
        doc += "\n例如:\n"
        doc += "- `cpp-style://best-practices/memory` - 内存管理最佳实践\n"
        doc += "- `cpp-style://best-practices/exceptions` - 异常处理最佳实践\n"
        doc += "- `cpp-style://best-practices/modern_cpp` - 现代 C++ 特性\n"

        return doc

    def _get_related_resources(self, topic: str) -> str:
        """获取相关资源链接"""
        doc = "## 相关资源\n\n"

        if topic == "memory":
            doc += "- C++ Core Guidelines: [资源管理](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)\n"
            doc += "- [RAII 和智能指针详解](https://en.cppreference.com/w/cpp/memory)\n"
            doc += "- 相关工具: Valgrind, AddressSanitizer\n"

        elif topic == "exceptions":
            doc += "- C++ Core Guidelines: [错误处理](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-errors)\n"
            doc += "- [异常安全性保证](https://en.cppreference.com/w/cpp/language/exceptions)\n"

        elif topic == "templates":
            doc += "- [C++ 模板完全指南](https://en.cppreference.com/w/cpp/language/templates)\n"
            doc += "- C++ Core Guidelines: [模板和泛型编程](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-templates)\n"

        elif topic == "concurrency":
            doc += "- C++ Core Guidelines: [并发](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-concurrency)\n"
            doc += "- [C++ 并发编程指南](https://en.cppreference.com/w/cpp/thread)\n"
            doc += "- 推荐阅读: 《C++ Concurrency in Action》\n"

        elif topic == "performance":
            doc += "- C++ Core Guidelines: [性能](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-performance)\n"
            doc += "- 性能分析工具: perf, gprof, Valgrind Callgrind\n"
            doc += "- [编译器优化技巧](https://en.cppreference.com/w/cpp/language/attributes)\n"

        elif topic == "modern_cpp":
            doc += "- 参考资源 `cpp-style://standard/cpp11` - C++11 特性\n"
            doc += "- 参考资源 `cpp-style://standard/cpp17` - C++17 特性\n"
            doc += "- 参考资源 `cpp-style://standard/cpp20` - C++20 特性\n"

        else:
            doc += "- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)\n"
            doc += "- [cppreference.com](https://en.cppreference.com/)\n"

        return doc


# 全局实例
_resource = None

def get_resource() -> BestPracticesResource:
    """获取全局资源实例"""
    global _resource
    if _resource is None:
        _resource = BestPracticesResource()
    return _resource
