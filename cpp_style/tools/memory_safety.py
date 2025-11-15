"""C++ 内存安全分析工具"""

import re
from typing import List, Tuple, Dict


class MemorySafetyAnalyzer:
    """内存安全分析器"""

    def analyze_memory_safety(self, code: str) -> Tuple[List[Dict], str]:
        """
        分析代码中的内存安全问题

        Args:
            code: 要分析的 C++ 代码

        Returns:
            (问题列表, 格式化的分析报告)
        """
        issues = []

        # 检查各种内存安全问题
        issues.extend(self._check_raw_pointers(code))
        issues.extend(self._check_manual_memory(code))
        issues.extend(self._check_array_access(code))
        issues.extend(self._check_string_operations(code))
        issues.extend(self._check_resource_leaks(code))
        issues.extend(self._check_double_delete(code))
        issues.extend(self._check_dangling_pointers(code))

        # 生成报告
        report = self._generate_report(issues, code)

        return issues, report

    def _check_raw_pointers(self, code: str) -> List[Dict]:
        """检查裸指针使用"""
        issues = []

        # 检查 new 操作符
        new_pattern = re.compile(r'\bnew\s+\w+')
        for match in new_pattern.finditer(code):
            issues.append({
                "type": "raw_pointer",
                "severity": "warning",
                "message": "使用了裸指针 new 操作符",
                "suggestion": "考虑使用 std::unique_ptr 或 std::shared_ptr",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        # 检查 T* 裸指针声明（排除函数参数）
        pointer_pattern = re.compile(r'(?<!std::)\b(\w+)\s*\*\s*(\w+)\s*=')
        for match in pointer_pattern.finditer(code):
            type_name = match.group(1)
            var_name = match.group(2)
            # 排除常见的智能指针和迭代器
            if type_name not in ['unique_ptr', 'shared_ptr', 'weak_ptr', 'auto']:
                issues.append({
                    "type": "raw_pointer_declaration",
                    "severity": "info",
                    "message": f"裸指针声明: {type_name}* {var_name}",
                    "suggestion": "如果拥有所有权，使用智能指针；如果只是观察，考虑使用引用",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_manual_memory(self, code: str) -> List[Dict]:
        """检查手动内存管理"""
        issues = []

        # 检查 delete
        delete_pattern = re.compile(r'\bdelete\s+\w+')
        for match in delete_pattern.finditer(code):
            issues.append({
                "type": "manual_delete",
                "severity": "warning",
                "message": "手动 delete 操作",
                "suggestion": "使用 RAII 和智能指针自动管理内存",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        # 检查 delete[]
        delete_array_pattern = re.compile(r'\bdelete\[\]\s+\w+')
        for match in delete_array_pattern.finditer(code):
            issues.append({
                "type": "manual_delete_array",
                "severity": "warning",
                "message": "手动 delete[] 操作",
                "suggestion": "使用 std::vector 或 std::array 替代动态数组",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        # 检查 malloc/free
        malloc_pattern = re.compile(r'\b(malloc|calloc|realloc)\s*\(')
        for match in malloc_pattern.finditer(code):
            issues.append({
                "type": "c_style_allocation",
                "severity": "error",
                "message": f"使用了 C 风格的内存分配: {match.group(1)}",
                "suggestion": "在 C++ 中使用 new/delete 或更好的智能指针",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        free_pattern = re.compile(r'\bfree\s*\(')
        for match in free_pattern.finditer(code):
            issues.append({
                "type": "c_style_free",
                "severity": "error",
                "message": "使用了 C 风格的 free",
                "suggestion": "在 C++ 中使用 delete 或智能指针",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        return issues

    def _check_array_access(self, code: str) -> List[Dict]:
        """检查数组访问"""
        issues = []

        # 检查 C 风格数组
        c_array_pattern = re.compile(r'\b(\w+)\s+(\w+)\s*\[\s*(\d+|\w+)\s*\]')
        for match in c_array_pattern.finditer(code):
            type_name = match.group(1)
            var_name = match.group(2)
            if type_name not in ['std', 'string', 'vector', 'array']:
                issues.append({
                    "type": "c_style_array",
                    "severity": "info",
                    "message": f"C 风格数组: {type_name} {var_name}[...]",
                    "suggestion": "考虑使用 std::array 或 std::vector",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        # 检查不安全的数组访问（使用 []）
        # 这是一个简化的检查，实际需要更复杂的分析
        array_access_pattern = re.compile(r'\w+\s*\[\s*\w+\s*\](?!\s*=\s*\{)')
        unsafe_access_count = len(array_access_pattern.findall(code))
        if unsafe_access_count > 0:
            issues.append({
                "type": "array_access",
                "severity": "info",
                "message": f"发现 {unsafe_access_count} 处数组下标访问",
                "suggestion": "确保边界检查，或使用 .at() 方法（会抛出异常）",
                "location": "multiple locations",
                "line": 0
            })

        return issues

    def _check_string_operations(self, code: str) -> List[Dict]:
        """检查不安全的字符串操作"""
        issues = []

        # 检查不安全的 C 字符串函数
        unsafe_funcs = {
            'strcpy': 'strncpy 或 std::string',
            'strcat': 'strncat 或 std::string',
            'sprintf': 'snprintf 或 std::format (C++20)',
            'gets': 'fgets 或 std::getline',
            'scanf': 'std::cin 或带边界检查的版本'
        }

        for func, suggestion in unsafe_funcs.items():
            pattern = re.compile(rf'\b{func}\s*\(')
            for match in pattern.finditer(code):
                issues.append({
                    "type": "unsafe_string_function",
                    "severity": "error",
                    "message": f"不安全的字符串函数: {func}",
                    "suggestion": f"使用 {suggestion}",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_resource_leaks(self, code: str) -> List[Dict]:
        """检查潜在的资源泄漏"""
        issues = []

        # 检查 fopen 但没有 fclose
        if re.search(r'\bfopen\s*\(', code):
            if not re.search(r'\bfclose\s*\(', code):
                issues.append({
                    "type": "resource_leak",
                    "severity": "warning",
                    "message": "使用了 fopen 但可能缺少 fclose",
                    "suggestion": "使用 RAII 包装器或 std::fstream",
                    "location": "fopen",
                    "line": 0
                })

        # 检查 new 但没有 delete
        new_count = len(re.findall(r'\bnew\s+\w+', code))
        delete_count = len(re.findall(r'\bdelete\s+', code))
        if new_count > delete_count:
            issues.append({
                "type": "potential_leak",
                "severity": "warning",
                "message": f"new 次数 ({new_count}) 多于 delete 次数 ({delete_count})",
                "suggestion": "检查是否有内存泄漏，或使用智能指针",
                "location": "code analysis",
                "line": 0
            })

        return issues

    def _check_double_delete(self, code: str) -> List[Dict]:
        """检查可能的双重释放"""
        issues = []

        # 检查 delete 后未置空
        delete_pattern = re.compile(r'\bdelete\s+(\w+)\s*;')
        for match in delete_pattern.finditer(code):
            var_name = match.group(1)
            # 检查后续是否有 = nullptr
            rest_code = code[match.end():]
            if not re.search(rf'\b{var_name}\s*=\s*nullptr', rest_code[:100]):
                issues.append({
                    "type": "no_nullptr_after_delete",
                    "severity": "warning",
                    "message": f"delete {var_name} 后未设置为 nullptr",
                    "suggestion": f"在 delete 后添加: {var_name} = nullptr;",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_dangling_pointers(self, code: str) -> List[Dict]:
        """检查悬空指针风险"""
        issues = []

        # 检查返回局部变量的地址
        return_address_pattern = re.compile(r'return\s+&\w+')
        for match in return_address_pattern.finditer(code):
            issues.append({
                "type": "return_local_address",
                "severity": "error",
                "message": "可能返回局部变量的地址",
                "suggestion": "返回值或使用智能指针，不要返回局部变量的地址",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })

        return issues

    def _generate_report(self, issues: List[Dict], code: str) -> str:
        """生成格式化的分析报告"""
        if not issues:
            return """
# ✅ 内存安全分析报告

**结果**: 未发现明显的内存安全问题！

**建议**:
- 继续保持良好的编码习惯
- 定期使用静态分析工具（如 clang-tidy, cppcheck）
- 运行时使用内存检测工具（如 Valgrind, AddressSanitizer）
"""

        # 按严重程度分类
        errors = [i for i in issues if i['severity'] == 'error']
        warnings = [i for i in issues if i['severity'] == 'warning']
        infos = [i for i in issues if i['severity'] == 'info']

        report = "# 🔍 内存安全分析报告\n\n"
        report += f"**分析结果**: 发现 {len(issues)} 个潜在问题\n"
        report += f"- 🔴 严重: {len(errors)}\n"
        report += f"- 🟡 警告: {len(warnings)}\n"
        report += f"- 🔵 信息: {len(infos)}\n\n"

        report += "---\n\n"

        # 报告错误
        if errors:
            report += "## 🔴 严重问题\n\n"
            for i, issue in enumerate(errors, 1):
                report += self._format_issue(i, issue)

        # 报告警告
        if warnings:
            report += "## 🟡 警告\n\n"
            for i, issue in enumerate(warnings, 1):
                report += self._format_issue(i, issue)

        # 报告信息
        if infos:
            report += "## 🔵 建议改进\n\n"
            for i, issue in enumerate(infos, 1):
                report += self._format_issue(i, issue)

        # 总体建议
        report += "\n## 💡 总体建议\n\n"
        report += "1. **使用智能指针**: 用 `std::unique_ptr` 和 `std::shared_ptr` 替代裸指针\n"
        report += "2. **遵循 RAII**: 利用对象生命周期自动管理资源\n"
        report += "3. **避免手动内存管理**: 使用标准容器（`std::vector`, `std::string`）\n"
        report += "4. **使用现代 C++ 特性**: 如 `std::optional`, `std::variant`\n"
        report += "5. **静态分析工具**: 使用 clang-tidy, cppcheck 进行深度检查\n"
        report += "6. **动态分析工具**: 使用 Valgrind, AddressSanitizer 检测运行时问题\n"

        return report

    def _format_issue(self, index: int, issue: Dict) -> str:
        """格式化单个问题"""
        output = f"### {index}. {issue['message']}\n\n"
        if issue.get('line', 0) > 0:
            output += f"**位置**: 第 {issue['line']} 行\n"
        if issue.get('location') != 'multiple locations':
            output += f"**代码**: `{issue['location']}`\n"
        output += f"**建议**: {issue['suggestion']}\n\n"
        return output


# 全局实例
_analyzer = None

def get_analyzer() -> MemorySafetyAnalyzer:
    """获取全局内存安全分析器实例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = MemorySafetyAnalyzer()
    return _analyzer
