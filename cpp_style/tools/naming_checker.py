"""C++ 命名规范检查工具"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple


class NamingChecker:
    """C++ 命名规范检查器"""

    def __init__(self):
        """加载命名规范数据"""
        data_path = Path(__file__).parent.parent / "data" / "naming_conventions.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            self.conventions = json.load(f)

    def check_naming(self, identifier: str, category: str) -> Tuple[bool, str, List[str]]:
        """
        检查标识符命名是否符合规范

        Args:
            identifier: 要检查的标识符
            category: 类别 (variable, constant, function, class, namespace,
                     member_variable, template_parameter, file_naming)

        Returns:
            (是否符合规范, 详细说明, 建议列表)
        """
        if category not in self.conventions:
            return False, f"未知的类别: {category}", []

        conv = self.conventions[category]
        style = conv["style"]

        # 根据不同风格进行检查
        is_valid, message = self._check_style(identifier, style, category)

        suggestions = []
        if not is_valid:
            suggestions = self._generate_suggestions(identifier, style, category)

        # 构建详细说明
        details = f"类别: {category}\n"
        details += f"推荐风格: {style}\n"
        details += f"标识符: {identifier}\n"
        details += f"检查结果: {'✓ 符合规范' if is_valid else '✗ 不符合规范'}\n"
        if message:
            details += f"说明: {message}\n"
        if suggestions:
            details += f"\n建议的命名:\n"
            for sug in suggestions:
                details += f"  • {sug}\n"

        # 添加规则说明
        details += f"\n规范要求:\n"
        for rule in conv.get("rules", []):
            details += f"  • {rule}\n"

        # 添加示例
        if "examples" in conv:
            details += f"\n正确示例: {', '.join(conv['examples']['good'])}\n"
            details += f"错误示例: {', '.join(conv['examples']['bad'])}\n"

        return is_valid, details, suggestions

    def _check_style(self, identifier: str, style: str, category: str) -> Tuple[bool, str]:
        """检查标识符是否符合指定风格"""

        # snake_case: 小写字母和下划线
        if "snake_case" in style.lower():
            if re.match(r'^[a-z][a-z0-9_]*$', identifier):
                return True, "符合 snake_case 风格"
            return False, "应使用小写字母和下划线"

        # UPPER_SNAKE_CASE: 大写字母和下划线
        if "UPPER_SNAKE_CASE" in style or "upper" in style.lower():
            if re.match(r'^[A-Z][A-Z0-9_]*$', identifier):
                return True, "符合 UPPER_SNAKE_CASE 风格"
            # 如果是 constant 类别，也检查 kCamelCase
            if category == "constant" and re.match(r'^k[A-Z][a-zA-Z0-9]*$', identifier):
                return True, "符合 kCamelCase 风格（Google Style）"
            return False, "常量应使用 UPPER_SNAKE_CASE 或 kCamelCase"

        # PascalCase/CamelCase: 大驼峰
        if "PascalCase" in style or "CamelCase" in style:
            if re.match(r'^[A-Z][a-zA-Z0-9]*$', identifier):
                return True, "符合 PascalCase 风格"
            return False, "应使用大驼峰命名（首字母大写）"

        # camelCase: 小驼峰
        if "camelCase" in style:
            if re.match(r'^[a-z][a-zA-Z0-9]*$', identifier):
                return True, "符合 camelCase 风格"
            return False, "应使用小驼峰命名（首字母小写）"

        # member_variable: 下划线后缀或 m_ 前缀
        if category == "member_variable":
            if identifier.endswith('_') or identifier.startswith('m_'):
                return True, "符合成员变量命名规范"
            return False, "成员变量应使用下划线后缀或 m_ 前缀"

        # template_parameter: 单个大写字母或 PascalCase
        if category == "template_parameter":
            if re.match(r'^[A-Z]$', identifier) or re.match(r'^T[A-Z][a-zA-Z0-9]*$', identifier):
                return True, "符合模板参数命名规范"
            return False, "模板参数应使用单个大写字母或 T 开头的大驼峰"

        # lowercase: 全小写
        if "lowercase" in style:
            if re.match(r'^[a-z][a-z0-9_]*$', identifier):
                return True, "符合小写命名风格"
            return False, "应使用全小写字母"

        return True, "符合规范"

    def _generate_suggestions(self, identifier: str, style: str, category: str) -> List[str]:
        """生成命名建议"""
        suggestions = []

        # 转换为 snake_case
        if "snake_case" in style:
            snake = self._to_snake_case(identifier)
            if snake != identifier:
                suggestions.append(snake)

        # 转换为 UPPER_SNAKE_CASE
        if "UPPER_SNAKE_CASE" in style:
            upper_snake = self._to_snake_case(identifier).upper()
            if upper_snake != identifier:
                suggestions.append(upper_snake)
            # 也提供 kCamelCase 选项
            if category == "constant":
                k_camel = "k" + self._to_pascal_case(identifier)
                suggestions.append(k_camel)

        # 转换为 PascalCase
        if "PascalCase" in style:
            pascal = self._to_pascal_case(identifier)
            if pascal != identifier:
                suggestions.append(pascal)

        # 转换为 camelCase
        if "camelCase" in style:
            camel = self._to_camel_case(identifier)
            if camel != identifier:
                suggestions.append(camel)

        # member_variable 特殊处理
        if category == "member_variable":
            if not identifier.endswith('_'):
                suggestions.append(identifier + '_')
            if not identifier.startswith('m_'):
                suggestions.append('m_' + identifier)

        return suggestions[:3]  # 最多返回3个建议

    def _to_snake_case(self, name: str) -> str:
        """转换为 snake_case"""
        # 移除前缀和后缀
        name = name.strip('_')
        if name.startswith('m_'):
            name = name[2:]
        if name.startswith('k') and len(name) > 1 and name[1].isupper():
            name = name[1:]

        # 在大写字母前插入下划线
        result = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        result = re.sub('([a-z0-9])([A-Z])', r'\1_\2', result)
        return result.lower()

    def _to_pascal_case(self, name: str) -> str:
        """转换为 PascalCase"""
        # 移除前缀和后缀
        name = name.strip('_')
        if name.startswith('m_'):
            name = name[2:]
        if name.startswith('k') and len(name) > 1 and name[1].isupper():
            return name[1:]  # 已经是 PascalCase

        # 分割单词并转换
        words = re.split(r'[_\s]+', name)
        return ''.join(word.capitalize() for word in words if word)

    def _to_camel_case(self, name: str) -> str:
        """转换为 camelCase"""
        pascal = self._to_pascal_case(name)
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return name


# 全局实例
_checker = None

def get_checker() -> NamingChecker:
    """获取全局命名检查器实例"""
    global _checker
    if _checker is None:
        _checker = NamingChecker()
    return _checker
