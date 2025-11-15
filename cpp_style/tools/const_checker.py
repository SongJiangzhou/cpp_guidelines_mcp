"""C++ const 正确性检查工具"""

import re
from typing import List, Dict, Tuple


class ConstCorrectnessChecker:
    """const 正确性检查器"""

    def check_const_correctness(self, code: str) -> Tuple[List[Dict], str]:
        """
        检查代码中的 const 正确性

        Args:
            code: 要检查的 C++ 代码

        Returns:
            (问题列表, 格式化的检查报告)
        """
        issues = []

        # 检查各种 const 使用问题
        issues.extend(self._check_member_functions(code))
        issues.extend(self._check_parameters(code))
        issues.extend(self._check_return_values(code))
        issues.extend(self._check_variables(code))
        issues.extend(self._check_pointers_refs(code))

        # 生成报告
        report = self._generate_report(issues)

        return issues, report

    def _check_member_functions(self, code: str) -> List[Dict]:
        """检查成员函数的 const 正确性"""
        issues = []

        # 检查 getter 函数是否是 const
        getter_pattern = re.compile(r'(\w+)\s+(get\w+|is\w+|has\w+)\s*\(\s*\)\s*\{')
        for match in getter_pattern.finditer(code):
            func_name = match.group(2)
            # 检查是否有 const 关键字
            full_line = code[max(0, match.start() - 50):match.end()]
            if 'const' not in full_line:
                issues.append({
                    "type": "missing_const_member",
                    "severity": "warning",
                    "message": f"getter 函数 {func_name}() 应该是 const",
                    "suggestion": f"在函数声明后添加 const: {func_name}() const",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        # 检查不修改成员的函数
        method_pattern = re.compile(r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{([^}]*)\}', re.DOTALL)
        for match in method_pattern.finditer(code):
            return_type = match.group(1)
            func_name = match.group(2)
            func_body = match.group(3)

            # 跳过构造函数、析构函数、运算符重载
            if func_name in ['if', 'for', 'while'] or func_name.startswith('operator'):
                continue

            # 检查函数体是否修改成员
            if not re.search(r'\w+\s*=', func_body) and 'const' not in code[match.start():match.end()]:
                # 可能应该是 const
                issues.append({
                    "type": "potentially_const_member",
                    "severity": "info",
                    "message": f"函数 {func_name}() 可能应该是 const",
                    "suggestion": "检查是否修改成员变量，如果不修改则添加 const",
                    "location": f"{return_type} {func_name}()",
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_parameters(self, code: str) -> List[Dict]:
        """检查函数参数的 const 正确性"""
        issues = []

        # 检查大对象参数是否使用 const 引用
        param_pattern = re.compile(r'(\w+(?:<[^>]+>)?)\s+(\w+)\s*[,)]')
        for match in param_pattern.finditer(code):
            param_type = match.group(1)
            param_name = match.group(2)

            # 检查是否是大对象类型
            large_types = ['string', 'vector', 'map', 'set', 'list', 'deque', 'unordered_map', 'unordered_set']
            is_large = any(t in param_type.lower() for t in large_types)

            if is_large and '&' not in code[match.start():match.end() + 20]:
                issues.append({
                    "type": "missing_const_ref_param",
                    "severity": "warning",
                    "message": f"参数 {param_name} 应该使用 const 引用传递",
                    "suggestion": f"const {param_type}& {param_name}",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        # 检查引用参数是否缺少 const
        ref_param_pattern = re.compile(r'(\w+)\s*&\s*(\w+)\s*[,)]')
        for match in ref_param_pattern.finditer(code):
            # 检查前面是否有 const
            prefix = code[max(0, match.start() - 10):match.start()]
            if 'const' not in prefix:
                param_type = match.group(1)
                param_name = match.group(2)
                issues.append({
                    "type": "non_const_ref_param",
                    "severity": "info",
                    "message": f"引用参数 {param_name} 可能应该是 const",
                    "suggestion": f"如果不修改参数，使用 const {param_type}& {param_name}",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_return_values(self, code: str) -> List[Dict]:
        """检查返回值的 const 正确性"""
        issues = []

        # 检查返回指针是否应该是 const
        return_ptr_pattern = re.compile(r'return\s+(\w+)\s*;')
        for match in return_ptr_pattern.finditer(code):
            var_name = match.group(1)
            # 查找函数签名
            func_start = code.rfind('(', 0, match.start())
            if func_start > 0:
                func_sig = code[max(0, func_start - 100):func_start]
                if '*' in func_sig and 'const' not in func_sig:
                    issues.append({
                        "type": "non_const_return_ptr",
                        "severity": "info",
                        "message": "返回指针可能应该是 const",
                        "suggestion": "如果不应修改返回的对象，返回 const T*",
                        "location": match.group(0),
                        "line": code[:match.start()].count('\n') + 1
                    })

        # 检查返回引用
        return_ref_pattern = re.compile(r'(\w+)\s*&\s+(\w+)\s*\([^)]*\)')
        for match in return_ref_pattern.finditer(code):
            return_type = match.group(1)
            func_name = match.group(2)
            # 检查是否有 const
            if 'const' not in code[max(0, match.start() - 10):match.start()]:
                issues.append({
                    "type": "non_const_return_ref",
                    "severity": "info",
                    "message": f"函数 {func_name} 返回引用可能应该是 const",
                    "suggestion": f"const {return_type}& {func_name}()",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_variables(self, code: str) -> List[Dict]:
        """检查变量的 const 正确性"""
        issues = []

        # 检查未修改的局部变量
        var_pattern = re.compile(r'(\w+)\s+(\w+)\s*=\s*([^;]+);')
        for match in var_pattern.finditer(code):
            var_type = match.group(1)
            var_name = match.group(2)

            # 跳过已经是 const 的
            if var_type == 'const' or 'const' in code[max(0, match.start() - 10):match.start()]:
                continue

            # 检查后续是否修改了这个变量
            rest_code = code[match.end():match.end() + 500]
            assignment_pattern = rf'\b{var_name}\s*='
            if not re.search(assignment_pattern, rest_code):
                issues.append({
                    "type": "missing_const_variable",
                    "severity": "info",
                    "message": f"变量 {var_name} 可能应该是 const",
                    "suggestion": f"const {var_type} {var_name} = ...",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _check_pointers_refs(self, code: str) -> List[Dict]:
        """检查指针和引用的 const 正确性"""
        issues = []

        # 检查指针的 const 位置
        ptr_pattern = re.compile(r'(\w+)\s*\*\s*(const)?\s*(\w+)')
        for match in ptr_pattern.finditer(code):
            type_name = match.group(1)
            const_after = match.group(2)
            var_name = match.group(3)

            # 检查是否有 const before *
            prefix = code[max(0, match.start() - 10):match.start()]
            const_before = 'const' in prefix

            if not const_before and not const_after:
                issues.append({
                    "type": "non_const_pointer",
                    "severity": "info",
                    "message": f"指针 {var_name} 缺少 const 限定",
                    "suggestion": "使用 const T* (指向const) 或 T* const (const指针) 或 const T* const (都是const)",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def _generate_report(self, issues: List[Dict]) -> str:
        """生成格式化的检查报告"""
        if not issues:
            return """
# ✅ const 正确性检查报告

**结果**: 代码的 const 使用看起来很好！

**const 最佳实践提醒**:
1. 不修改的成员函数应该声明为 const
2. 大对象参数使用 const 引用传递
3. 不修改的局部变量声明为 const
4. 正确使用 const T* (指向const) 和 T* const (const指针)
5. 返回内部数据时使用 const 引用或指针
"""

        # 按严重程度分类
        errors = [i for i in issues if i['severity'] == 'error']
        warnings = [i for i in issues if i['severity'] == 'warning']
        infos = [i for i in issues if i['severity'] == 'info']

        report = "# 🔍 const 正确性检查报告\n\n"
        report += f"**检查结果**: 发现 {len(issues)} 个潜在问题\n"
        report += f"- 🔴 错误: {len(errors)}\n"
        report += f"- 🟡 警告: {len(warnings)}\n"
        report += f"- 🔵 建议: {len(infos)}\n\n"

        report += "---\n\n"

        # 报告问题
        if warnings:
            report += "## 🟡 应该改进的地方\n\n"
            for i, issue in enumerate(warnings, 1):
                report += self._format_issue(i, issue)

        if infos:
            report += "## 🔵 可以改进的地方\n\n"
            for i, issue in enumerate(infos, 1):
                report += self._format_issue(i, issue)

        # const 使用指南
        report += "\n## 📚 const 使用指南\n\n"
        report += "### 成员函数\n"
        report += "```cpp\n"
        report += "class Widget {\n"
        report += "  int getValue() const;        // 不修改成员\n"
        report += "  void setValue(int v);        // 修改成员\n"
        report += "  bool isEmpty() const;        // getter 应该是 const\n"
        report += "};\n"
        report += "```\n\n"

        report += "### 函数参数\n"
        report += "```cpp\n"
        report += "// 大对象使用 const 引用\n"
        report += "void process(const std::string& str);\n"
        report += "void process(const std::vector<int>& vec);\n\n"
        report += "// 小对象可以传值\n"
        report += "void process(int value);\n"
        report += "void process(std::string_view sv);  // C++17\n"
        report += "```\n\n"

        report += "### 指针的 const\n"
        report += "```cpp\n"
        report += "const int* p1;       // 指向 const int (不能通过 p1 修改)\n"
        report += "int* const p2;       // const 指针 (不能改变指向)\n"
        report += "const int* const p3; // 都是 const\n"
        report += "```\n\n"

        report += "### 返回值\n"
        report += "```cpp\n"
        report += "class Container {\n"
        report += "  const T& get(int i) const;  // 返回 const 引用\n"
        report += "  T& get(int i);              // 返回可修改引用\n"
        report += "};\n"
        report += "```\n"

        return report

    def _format_issue(self, index: int, issue: Dict) -> str:
        """格式化单个问题"""
        output = f"### {index}. {issue['message']}\n\n"
        if issue.get('line', 0) > 0:
            output += f"**位置**: 第 {issue['line']} 行\n"
        if issue.get('location'):
            output += f"**代码**: `{issue['location']}`\n"
        output += f"**建议**: {issue['suggestion']}\n\n"
        return output


# 全局实例
_checker = None

def get_checker() -> ConstCorrectnessChecker:
    """获取全局 const 正确性检查器实例"""
    global _checker
    if _checker is None:
        _checker = ConstCorrectnessChecker()
    return _checker
