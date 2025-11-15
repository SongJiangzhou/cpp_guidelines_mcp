"""C++ 命名规范资源"""

import json
from pathlib import Path
from typing import Optional


class NamingRulesResource:
    """命名规范资源提供器"""

    def __init__(self):
        """加载命名规范数据"""
        data_path = Path(__file__).parent.parent / "data" / "naming_conventions.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            self.conventions = json.load(f)

    def get_naming_rule(self, category: str) -> str:
        """
        获取指定类别的命名规范

        Args:
            category: 类别名称 (variable, constant, function, class, etc.)

        Returns:
            格式化的命名规范文档
        """
        if category not in self.conventions:
            available = ', '.join(self.conventions.keys())
            return f"未知的类别: {category}\n\n可用类别: {available}"

        conv = self.conventions[category]

        # 构建格式化的文档
        doc = f"# C++ 命名规范: {category.upper()}\n\n"

        # 风格说明
        doc += f"## 推荐风格\n"
        doc += f"{conv['style']}\n\n"

        # 描述
        doc += f"## 描述\n"
        doc += f"{conv['description']}\n\n"

        # 示例
        if "examples" in conv:
            doc += f"## 正确示例\n"
            for example in conv['examples']['good']:
                doc += f"✓ `{example}`\n"
            doc += f"\n## 错误示例\n"
            for example in conv['examples']['bad']:
                doc += f"✗ `{example}`\n"
            doc += "\n"

        # 规则
        if "rules" in conv:
            doc += f"## 详细规则\n"
            for i, rule in enumerate(conv['rules'], 1):
                doc += f"{i}. {rule}\n"
            doc += "\n"

        # 添加通用建议
        doc += self._get_general_advice(category)

        return doc

    def get_all_categories(self) -> str:
        """获取所有可用类别的概览"""
        doc = "# C++ 命名规范类别\n\n"
        doc += "以下是所有可用的命名规范类别：\n\n"

        for category, conv in self.conventions.items():
            doc += f"## {category}\n"
            doc += f"**风格**: {conv['style']}\n"
            doc += f"**说明**: {conv['description']}\n"
            if "examples" in conv and conv['examples']['good']:
                doc += f"**示例**: `{conv['examples']['good'][0]}`\n"
            doc += "\n"

        doc += "\n## 使用方式\n"
        doc += "使用资源 URI: `cpp-style://naming/{category}` 获取详细规范\n"
        doc += "\n例如:\n"
        doc += "- `cpp-style://naming/variable` - 变量命名规范\n"
        doc += "- `cpp-style://naming/function` - 函数命名规范\n"
        doc += "- `cpp-style://naming/class` - 类命名规范\n"

        return doc

    def _get_general_advice(self, category: str) -> str:
        """获取通用建议"""
        advice = "## 通用建议\n\n"

        if category == "variable":
            advice += "- 使用有意义的描述性名称\n"
            advice += "- 避免单字母名称（除了 i, j, k 用于循环）\n"
            advice += "- 布尔变量以 is、has、should 等开头\n"
            advice += "- 临时变量名要简短但清晰\n"

        elif category == "function":
            advice += "- 函数名应该是动词或动词短语\n"
            advice += "- 清楚地表达函数的作用\n"
            advice += "- getter 可以省略 get 前缀\n"
            advice += "- setter 使用 set 前缀\n"

        elif category == "class":
            advice += "- 类名应该是名词或名词短语\n"
            advice += "- 表达类的职责和作用\n"
            advice += "- 避免模糊的名称如 Manager、Handler\n"
            advice += "- 考虑使用领域驱动的命名\n"

        elif category == "constant":
            advice += "- 使用全大写表示编译期常量\n"
            advice += "- 使用 constexpr 替代 #define\n"
            advice += "- 枚举值建议使用 kCamelCase\n"

        elif category == "namespace":
            advice += "- 命名空间名称应该简短\n"
            advice += "- 避免嵌套过深\n"
            advice += "- 不要在头文件中使用 using namespace\n"

        else:
            advice += "- 保持一致性，遵循项目现有风格\n"
            advice += "- 清晰性优先于简洁性\n"
            advice += "- 参考主流风格指南（Google, LLVM, etc.）\n"

        return advice


# 全局实例
_resource = None

def get_resource() -> NamingRulesResource:
    """获取全局资源实例"""
    global _resource
    if _resource is None:
        _resource = NamingRulesResource()
    return _resource
