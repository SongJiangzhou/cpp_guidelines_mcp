中文 | [English](README.md)

# C++ 编码规范 MCP 服务器

对代码库强制执行一致的 C++ 编码规范和最佳实践。检查命名规范、内存安全和 const 正确性，并提供直到 C++23 的现代化改造建议。内置代码审查提示模板，快速访问精选规范文档。

## 工具列表

| 工具 | 说明 |
|------|------|
| `check_naming` | 检查 C++ 标识符（变量、类、函数等）是否符合命名规范 |
| `check_include_guard` | 验证头文件包含保护或 `#pragma once` 的正确性 |
| `analyze_memory_safety` | 检测内存泄漏、悬空指针和不安全的内存操作 |
| `suggest_modern_cpp` | 提供面向 C++11 至 C++23 的现代化改造建议 |
| `check_const_correctness` | 找出成员函数、参数和变量中缺失的 `const` 限定符 |

## 资源文档

| URI | 说明 |
|-----|------|
| `cpp-style://naming/{category}` | 命名规范参考（variable、class、function、namespace 等） |
| `cpp-style://best-practices/{topic}` | 最佳实践指南（memory、exceptions、templates、concurrency 等） |
| `cpp-style://standard/{version}` | C++ 标准特性文档（cpp11 – cpp23） |
| `cpp-style://examples/{pattern}` | 设计模式示例（RAII、Pimpl、Factory、Observer 等） |

## 提示模板

| 提示 | 说明 |
|------|------|
| `code_review` | 代码审查模板（综合 / 性能 / 安全 / 可读性 / 现代特性） |
| `refactor_suggestion` | 面向指定 C++ 标准的重构建议 |

## 快速开始

### 通过 Smithery 安装（推荐）

```bash
npx -y @smithery/cli install @SongJiangzhou/cpp_guidelines --client claude
```

### MCP 端点（HTTP / streamable-http）

```
https://cpp-style-guide-mcp.fly.dev/mcp
```

### 本地安装

```bash
git clone https://github.com/SongJiangzhou/cpp_guidelines_mcp.git
cd cpp_guidelines_mcp
uv sync
uv run mcp run cpp_style_server.py
```

添加到 MCP 客户端配置：

```json
{
  "mcpServers": {
    "cpp-style": {
      "command": "uv",
      "args": ["run", "mcp", "run", "cpp_style_server.py"],
      "cwd": "/path/to/cpp_guidelines_mcp"
    }
  }
}
```

## 使用示例

```
# 检查变量命名
check_naming("myVariable", "variable")

# 分析内存安全问题
analyze_memory_safety("void f(int* p) { delete p; p->run(); }")

# 升级代码到 C++17
suggest_modern_cpp("for (int i=0; i<v.size(); i++) {...}", "cpp17")

# 检查 const 正确性
check_const_correctness("class Foo { int getValue() { return x; } int x; };")

# 查看命名规范文档
资源：cpp-style://naming/all

# 查看内存管理最佳实践
资源：cpp-style://best-practices/memory
```

## 项目结构

```
cpp_guidelines_mcp/
├── cpp_style_server.py        # MCP 服务器入口
├── cpp_style/
│   ├── tools/                 # 5 个分析工具
│   ├── resources/             # 4 类规范文档
│   ├── prompts/               # 2 个提示模板
│   └── data/                  # JSON 知识库
├── fly.toml                   # Fly.io 部署配置
├── Dockerfile                 # 容器镜像
└── smithery.yaml              # Smithery 配置（本地 stdio 模式）
```

## 技术栈

- Python >= 3.12
- [FastMCP](https://github.com/jlowin/fastmcp) >= 1.21.0
- [uv](https://github.com/astral-sh/uv) 包管理器
- 部署于 [Fly.io](https://fly.io)

## 许可证

[MIT](LICENSE)

## 相关链接

- GitHub：https://github.com/SongJiangzhou/cpp_guidelines_mcp
- 问题反馈：https://github.com/SongJiangzhou/cpp_guidelines_mcp/issues
- Smithery：https://smithery.ai/server/SongJiangzhou/cpp_guidelines
