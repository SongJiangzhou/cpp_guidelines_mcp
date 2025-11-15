"""C++ 头文件包含保护检查工具"""

import re
from typing import Tuple, Optional, List
from pathlib import Path


class IncludeGuardChecker:
    """包含保护检查器"""

    def check_include_guard(
        self,
        code: str,
        file_path: Optional[str] = None
    ) -> Tuple[bool, str, List[str]]:
        """
        检查头文件的包含保护

        Args:
            code: 头文件代码
            file_path: 可选的文件路径，用于生成建议的保护宏名

        Returns:
            (是否符合规范, 详细说明, 建议列表)
        """
        lines = code.strip().split('\n')
        if len(lines) < 3:
            return False, "文件太短，无法包含有效的包含保护", []

        # 检查 #pragma once
        has_pragma_once = self._check_pragma_once(code)

        # 检查传统的 #ifndef/#define/#endif 保护
        has_traditional_guard, guard_name = self._check_traditional_guard(code)

        suggestions = []
        details = ""

        if has_pragma_once:
            details = "✓ 使用了 #pragma once\n\n"
            details += "说明: #pragma once 是现代编译器广泛支持的简洁方式。\n"
            details += "优点: 简洁、避免宏名冲突\n"
            details += "注意: 大多数编译器支持，但不是 C++ 标准的一部分\n"
            return True, details, []

        if has_traditional_guard:
            # 检查保护宏命名是否合理
            is_valid_name, name_message = self._validate_guard_name(guard_name, file_path)

            details = f"✓ 使用了传统的包含保护\n"
            details += f"保护宏名: {guard_name}\n\n"

            if is_valid_name:
                details += f"命名检查: ✓ 符合规范\n"
                details += f"{name_message}\n"
            else:
                details += f"命名检查: ✗ 可以改进\n"
                details += f"{name_message}\n\n"
                # 生成建议的宏名
                if file_path:
                    suggested_names = self._generate_guard_names(file_path)
                    suggestions = suggested_names
                    details += "建议的保护宏名:\n"
                    for name in suggested_names:
                        details += f"  • {name}\n"

            details += "\n包含保护规范:\n"
            details += "  • 宏名应全大写，使用下划线分隔\n"
            details += "  • 包含文件路径或项目名作为前缀，避免冲突\n"
            details += "  • 以 _H、_HPP 或 _H_ 结尾\n"
            details += "  • 避免以下划线开头（保留给编译器）\n"

            return True, details, suggestions

        # 没有任何保护
        details = "✗ 缺少包含保护！\n\n"
        details += "头文件应使用以下方式之一防止重复包含:\n\n"

        details += "方式1: #pragma once (推荐)\n"
        details += "```cpp\n"
        details += "#pragma once\n\n"
        details += "// 头文件内容\n"
        details += "```\n\n"

        details += "方式2: 传统包含保护\n"
        details += "```cpp\n"
        if file_path:
            guard_name = self._generate_guard_names(file_path)[0]
            suggestions = self._generate_guard_names(file_path)
        else:
            guard_name = "MY_HEADER_H"
        details += f"#ifndef {guard_name}\n"
        details += f"#define {guard_name}\n\n"
        details += "// 头文件内容\n\n"
        details += f"#endif // {guard_name}\n"
        details += "```\n"

        return False, details, suggestions

    def _check_pragma_once(self, code: str) -> bool:
        """检查是否使用 #pragma once"""
        return bool(re.search(r'^\s*#\s*pragma\s+once\s*$', code, re.MULTILINE))

    def _check_traditional_guard(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        检查传统的 #ifndef/#define/#endif 保护

        Returns:
            (是否存在, 保护宏名)
        """
        lines = code.split('\n')

        # 查找 #ifndef
        ifndef_pattern = re.compile(r'^\s*#\s*ifndef\s+([A-Z_][A-Z0-9_]*)\s*$')
        define_pattern = re.compile(r'^\s*#\s*define\s+([A-Z_][A-Z0-9_]*)\s*$')
        endif_pattern = re.compile(r'^\s*#\s*endif')

        ifndef_macro = None
        define_macro = None

        # 找到第一个 #ifndef（跳过注释）
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            match = ifndef_pattern.match(line)
            if match:
                ifndef_macro = match.group(1)
                break

        if not ifndef_macro:
            return False, None

        # 检查紧跟的 #define
        found_ifndef = False
        for line in lines:
            if found_ifndef:
                match = define_pattern.match(line)
                if match:
                    define_macro = match.group(1)
                    break
                # 如果不是空行或注释，则失败
                stripped = line.strip()
                if stripped and not stripped.startswith('//'):
                    break
            elif ifndef_pattern.match(line):
                found_ifndef = True

        # 检查 #ifndef 和 #define 的宏名是否一致
        if ifndef_macro and define_macro and ifndef_macro == define_macro:
            # 检查文件末尾是否有 #endif
            has_endif = False
            for line in reversed(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('//'):
                    if endif_pattern.match(line):
                        has_endif = True
                    break

            if has_endif:
                return True, ifndef_macro

        return False, None

    def _validate_guard_name(
        self,
        guard_name: str,
        file_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        验证保护宏名是否合理

        Returns:
            (是否有效, 说明信息)
        """
        issues = []

        # 检查是否以下划线开头（不推荐）
        if guard_name.startswith('_'):
            issues.append("不应以下划线开头（保留给编译器实现）")

        # 检查是否全大写
        if not guard_name.isupper():
            issues.append("应使用全大写字母")

        # 检查是否包含双下划线（不推荐）
        if '__' in guard_name:
            issues.append("不应包含连续的双下划线（保留标识符）")

        # 检查是否有合适的后缀
        valid_suffixes = ['_H', '_HPP', '_H_', '_INCLUDED']
        has_valid_suffix = any(guard_name.endswith(suffix) for suffix in valid_suffixes)
        if not has_valid_suffix:
            issues.append(f"建议以 {', '.join(valid_suffixes)} 之一结尾")

        # 检查长度
        if len(guard_name) < 5:
            issues.append("宏名太短，容易冲突")

        if issues:
            return False, "发现以下问题:\n  • " + "\n  • ".join(issues)
        else:
            return True, "命名符合规范"

    def _generate_guard_names(self, file_path: str) -> List[str]:
        """根据文件路径生成建议的保护宏名"""
        path = Path(file_path)
        suggestions = []

        # 获取文件名（不含扩展名）
        name = path.stem.upper()

        # 方案1: 简单的文件名 + _H
        suggestions.append(f"{name}_H")

        # 方案2: 文件名 + _HPP
        if path.suffix.lower() == '.hpp':
            suggestions.append(f"{name}_HPP")

        # 方案3: 包含父目录
        if len(path.parts) > 1:
            parent = path.parts[-2].upper()
            suggestions.append(f"{parent}_{name}_H")

        # 方案4: 完整路径（适合项目层级）
        # 例如: src/utils/helper.h -> SRC_UTILS_HELPER_H
        if len(path.parts) > 2:
            full_path = '_'.join(part.upper() for part in path.parts[:-1])
            suggestions.append(f"{full_path}_{name}_H")

        # 转换为合法的宏名（替换特殊字符）
        suggestions = [re.sub(r'[^A-Z0-9_]', '_', s) for s in suggestions]

        # 去重
        return list(dict.fromkeys(suggestions))[:3]


# 全局实例
_checker = None

def get_checker() -> IncludeGuardChecker:
    """获取全局包含保护检查器实例"""
    global _checker
    if _checker is None:
        _checker = IncludeGuardChecker()
    return _checker
