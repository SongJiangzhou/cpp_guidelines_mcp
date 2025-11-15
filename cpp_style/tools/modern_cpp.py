"""现代 C++ 建议工具"""

import re
from typing import List, Dict, Tuple


class ModernCppSuggester:
    """现代 C++ 建议器"""

    def suggest_modern_cpp(self, code: str, target_standard: str = "cpp17") -> Tuple[List[Dict], str]:
        """
        建议将代码升级为现代 C++ 写法

        Args:
            code: 要分析的 C++ 代码
            target_standard: 目标标准 (cpp11, cpp14, cpp17, cpp20, cpp23)

        Returns:
            (建议列表, 格式化的建议报告)
        """
        suggestions = []

        # 根据目标标准检查可用特性
        if target_standard in ['cpp11', 'cpp14', 'cpp17', 'cpp20', 'cpp23']:
            suggestions.extend(self._check_cpp11_features(code))

        if target_standard in ['cpp14', 'cpp17', 'cpp20', 'cpp23']:
            suggestions.extend(self._check_cpp14_features(code))

        if target_standard in ['cpp17', 'cpp20', 'cpp23']:
            suggestions.extend(self._check_cpp17_features(code))

        if target_standard in ['cpp20', 'cpp23']:
            suggestions.extend(self._check_cpp20_features(code))

        if target_standard == 'cpp23':
            suggestions.extend(self._check_cpp23_features(code))

        # 生成报告
        report = self._generate_report(suggestions, target_standard)

        return suggestions, report

    def _check_cpp11_features(self, code: str) -> List[Dict]:
        """检查可以使用 C++11 特性改进的代码"""
        suggestions = []

        # 检查 NULL vs nullptr
        if re.search(r'\bNULL\b', code) or re.search(r'=\s*0\s*;.*指针', code):
            suggestions.append({
                "standard": "C++11",
                "feature": "nullptr",
                "old_pattern": "NULL 或 0",
                "new_pattern": "nullptr",
                "example_old": "int* ptr = NULL;",
                "example_new": "int* ptr = nullptr;",
                "benefit": "类型安全，避免重载歧义"
            })

        # 检查传统 for 循环遍历容器
        if re.search(r'for\s*\(\s*\w+\s+\w+\s*=.*\.begin\(\)', code):
            suggestions.append({
                "standard": "C++11",
                "feature": "范围 for 循环",
                "old_pattern": "for (auto it = container.begin(); ...)",
                "new_pattern": "for (auto& item : container)",
                "example_old": "for (auto it = vec.begin(); it != vec.end(); ++it) { *it... }",
                "example_new": "for (auto& item : vec) { item... }",
                "benefit": "更简洁，避免迭代器错误"
            })

        # 检查裸指针 new
        if re.search(r'\bnew\s+\w+', code) and not re.search(r'make_unique|make_shared', code):
            suggestions.append({
                "standard": "C++11",
                "feature": "智能指针",
                "old_pattern": "Type* ptr = new Type()",
                "new_pattern": "auto ptr = std::make_unique<Type>()",
                "example_old": "Widget* w = new Widget();\n// ...\ndelete w;",
                "example_new": "auto w = std::make_unique<Widget>();\n// 自动释放",
                "benefit": "自动内存管理，防止泄漏"
            })

        # 检查 typedef vs using
        if re.search(r'\btypedef\s+', code):
            suggestions.append({
                "standard": "C++11",
                "feature": "using 别名",
                "old_pattern": "typedef ... TypeName;",
                "new_pattern": "using TypeName = ...;",
                "example_old": "typedef std::vector<int> IntVec;",
                "example_new": "using IntVec = std::vector<int>;",
                "benefit": "更清晰，支持模板别名"
            })

        # 检查虚函数重写
        if re.search(r'virtual\s+\w+.*\(.*\)\s*\{', code):
            if not re.search(r'override\b', code):
                suggestions.append({
                    "standard": "C++11",
                    "feature": "override 关键字",
                    "old_pattern": "virtual void func() { ... }",
                    "new_pattern": "void func() override { ... }",
                    "example_old": "class Derived : public Base {\n  virtual void draw() { ... }\n};",
                    "example_new": "class Derived : public Base {\n  void draw() override { ... }\n};",
                    "benefit": "编译器检查是否正确重写"
                })

        # 检查初始化列表
        if re.search(r'\bstd::vector<\w+>\s+\w+;\s*\w+\.push_back', code):
            suggestions.append({
                "standard": "C++11",
                "feature": "初始化列表",
                "old_pattern": "vector<int> v; v.push_back(1); v.push_back(2);",
                "new_pattern": "vector<int> v{1, 2};",
                "example_old": "std::vector<int> nums;\nnums.push_back(1);\nnums.push_back(2);",
                "example_new": "std::vector<int> nums{1, 2};",
                "benefit": "更简洁，性能更好"
            })

        # 检查是否可以使用 auto
        explicit_type_pattern = re.compile(r'(\w+(?:<[^>]+>)?)\s+(\w+)\s*=\s*\1')
        if explicit_type_pattern.search(code):
            suggestions.append({
                "standard": "C++11",
                "feature": "auto 类型推导",
                "old_pattern": "Type var = Type(...);",
                "new_pattern": "auto var = Type(...);",
                "example_old": "std::vector<int> vec = std::vector<int>();",
                "example_new": "auto vec = std::vector<int>();",
                "benefit": "减少冗余，提高可维护性"
            })

        return suggestions

    def _check_cpp14_features(self, code: str) -> List[Dict]:
        """检查可以使用 C++14 特性改进的代码"""
        suggestions = []

        # 检查是否使用了 new unique_ptr 而非 make_unique
        if re.search(r'unique_ptr<\w+>\(new\s+\w+', code):
            suggestions.append({
                "standard": "C++14",
                "feature": "std::make_unique",
                "old_pattern": "std::unique_ptr<T>(new T(...))",
                "new_pattern": "std::make_unique<T>(...)",
                "example_old": "auto ptr = std::unique_ptr<Widget>(new Widget(arg));",
                "example_new": "auto ptr = std::make_unique<Widget>(arg);",
                "benefit": "更简洁，异常安全"
            })

        # 检查 lambda 是否可以使用泛型参数
        if re.search(r'\[\]\s*\(\s*\w+\s+\w+\s*\)', code):
            suggestions.append({
                "standard": "C++14",
                "feature": "泛型 lambda",
                "old_pattern": "[](Type x) { ... }",
                "new_pattern": "[](auto x) { ... }",
                "example_old": "[](int x) { return x * 2; }",
                "example_new": "[](auto x) { return x * 2; }",
                "benefit": "更通用，代码复用"
            })

        return suggestions

    def _check_cpp17_features(self, code: str) -> List[Dict]:
        """检查可以使用 C++17 特性改进的代码"""
        suggestions = []

        # 检查 pair/tuple 解包
        if re.search(r'\.first|\.second', code):
            suggestions.append({
                "standard": "C++17",
                "feature": "结构化绑定",
                "old_pattern": "auto p = map.insert(...); p.first...; p.second...;",
                "new_pattern": "auto [it, success] = map.insert(...);",
                "example_old": "auto result = map.insert({key, value});\nif (result.second) { use(result.first); }",
                "example_new": "auto [it, inserted] = map.insert({key, value});\nif (inserted) { use(it); }",
                "benefit": "更清晰，避免 .first/.second"
            })

        # 检查 if 中的临时变量
        if re.search(r'auto\s+\w+\s*=.*;\s*if\s*\(\s*\w+', code):
            suggestions.append({
                "standard": "C++17",
                "feature": "if 初始化语句",
                "old_pattern": "auto x = get(); if (x) { ... }",
                "new_pattern": "if (auto x = get(); x) { ... }",
                "example_old": "auto it = map.find(key);\nif (it != map.end()) { use(it); }",
                "example_new": "if (auto it = map.find(key); it != map.end()) { use(it); }",
                "benefit": "限制作用域，更清晰"
            })

        # 检查是否可以使用 std::optional
        if re.search(r'(bool.*found|return.*nullptr)', code):
            suggestions.append({
                "standard": "C++17",
                "feature": "std::optional",
                "old_pattern": "返回 nullptr 或布尔标志",
                "new_pattern": "std::optional<T>",
                "example_old": "int* find(int key) {\n  if (...) return &value;\n  return nullptr;\n}",
                "example_new": "std::optional<int> find(int key) {\n  if (...) return value;\n  return std::nullopt;\n}",
                "benefit": "明确表达可能不存在的值"
            })

        # 检查字符串参数
        if re.search(r'const\s+std::string\s*&', code):
            suggestions.append({
                "standard": "C++17",
                "feature": "std::string_view",
                "old_pattern": "const std::string&",
                "new_pattern": "std::string_view",
                "example_old": "void process(const std::string& str);",
                "example_new": "void process(std::string_view str);",
                "benefit": "避免拷贝，支持多种字符串类型"
            })

        return suggestions

    def _check_cpp20_features(self, code: str) -> List[Dict]:
        """检查可以使用 C++20 特性改进的代码"""
        suggestions = []

        # 检查模板约束
        if re.search(r'template\s*<\s*typename\s+T\s*>', code):
            suggestions.append({
                "standard": "C++20",
                "feature": "Concepts",
                "old_pattern": "template<typename T>",
                "new_pattern": "template<std::integral T>",
                "example_old": "template<typename T>\nT add(T a, T b) { return a + b; }",
                "example_new": "template<std::integral T>\nT add(T a, T b) { return a + b; }",
                "benefit": "更清晰的错误信息，明确约束"
            })

        # 检查手动比较运算符
        if re.search(r'bool\s+operator<|bool\s+operator==', code):
            suggestions.append({
                "standard": "C++20",
                "feature": "三路比较运算符 (<=>)",
                "old_pattern": "手动实现所有比较运算符",
                "new_pattern": "auto operator<=>(const T&) const = default;",
                "example_old": "bool operator<(const Point& p) const { ... }\nbool operator==(const Point& p) const { ... }",
                "example_new": "auto operator<=>(const Point&) const = default;",
                "benefit": "自动生成所有比较运算符"
            })

        # 检查容器连续序列
        if re.search(r'\.data\(\).*\.size\(\)', code):
            suggestions.append({
                "standard": "C++20",
                "feature": "std::span",
                "old_pattern": "传递指针和大小",
                "new_pattern": "std::span<T>",
                "example_old": "void process(int* data, size_t size);",
                "example_new": "void process(std::span<int> data);",
                "benefit": "更安全，包含大小信息"
            })

        return suggestions

    def _check_cpp23_features(self, code: str) -> List[Dict]:
        """检查可以使用 C++23 特性改进的代码"""
        suggestions = []

        # 检查错误处理
        if re.search(r'(throw|try|catch)', code):
            suggestions.append({
                "standard": "C++23",
                "feature": "std::expected",
                "old_pattern": "异常或错误码",
                "new_pattern": "std::expected<T, Error>",
                "example_old": "int divide(int a, int b) {\n  if (b == 0) throw std::runtime_error(\"div by 0\");\n  return a / b;\n}",
                "example_new": "std::expected<int, Error> divide(int a, int b) {\n  if (b == 0) return std::unexpected(Error::DivByZero);\n  return a / b;\n}",
                "benefit": "明确的错误处理，避免异常开销"
            })

        # 检查 printf 风格
        if re.search(r'printf|cout\s*<<', code):
            suggestions.append({
                "standard": "C++23",
                "feature": "std::print",
                "old_pattern": "printf 或 cout",
                "new_pattern": "std::print",
                "example_old": "std::cout << \"Hello, \" << name << \"!\" << std::endl;",
                "example_new": "std::print(\"Hello, {}!\\n\", name);",
                "benefit": "类型安全，更简洁"
            })

        return suggestions

    def _generate_report(self, suggestions: List[Dict], target_standard: str) -> str:
        """生成格式化的建议报告"""
        if not suggestions:
            return f"""
# ✅ 现代 C++ 分析报告

**目标标准**: {target_standard.upper()}

**结果**: 代码已经很现代了！未发现明显的改进点。

**提示**: 继续保持使用现代 C++ 特性的好习惯！
"""

        report = f"# 🚀 现代 C++ 升级建议\n\n"
        report += f"**目标标准**: {target_standard.upper()}\n"
        report += f"**发现**: {len(suggestions)} 个改进建议\n\n"
        report += "---\n\n"

        # 按标准分组
        by_standard = {}
        for sug in suggestions:
            std = sug['standard']
            if std not in by_standard:
                by_standard[std] = []
            by_standard[std].append(sug)

        # 生成报告
        for std in ['C++11', 'C++14', 'C++17', 'C++20', 'C++23']:
            if std in by_standard:
                report += f"## {std} 特性\n\n"
                for i, sug in enumerate(by_standard[std], 1):
                    report += f"### {i}. {sug['feature']}\n\n"
                    report += f"**旧写法**:\n```cpp\n{sug['example_old']}\n```\n\n"
                    report += f"**新写法**:\n```cpp\n{sug['example_new']}\n```\n\n"
                    report += f"**优势**: {sug['benefit']}\n\n"
                    report += "---\n\n"

        # 总结
        report += "## 💡 总结\n\n"
        report += f"通过采用 {target_standard.upper()} 的特性，你可以：\n"
        report += "- ✨ 提高代码可读性和简洁性\n"
        report += "- 🛡️ 增强类型安全和异常安全\n"
        report += "- ⚡ 提升性能（编译期优化）\n"
        report += "- 🔧 减少维护成本\n"

        return report


# 全局实例
_suggester = None

def get_suggester() -> ModernCppSuggester:
    """获取全局现代 C++ 建议器实例"""
    global _suggester
    if _suggester is None:
        _suggester = ModernCppSuggester()
    return _suggester
