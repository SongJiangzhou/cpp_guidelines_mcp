# C++ Style Guide MCP Server

[![smithery badge](https://smithery.ai/badge/@SongJiangzhou/cpp_guidelines)](https://smithery.ai/server/@SongJiangzhou/cpp_guidelines)

专业的 C++ 编码规范检查和最佳实践建议工具，基于 MCP (Model Context Protocol) 协议构建。

## 功能特性

**5 个代码分析工具**
- `check_naming` - 检查命名规范（变量、函数、类等）
- `check_include_guard` - 验证头文件包含保护
- `analyze_memory_safety` - 检测内存泄漏和悬空指针
- `suggest_modern_cpp` - 现代 C++ 升级建议 (C++11/14/17/20/23)
- `check_const_correctness` - 检查 const 正确性

**4 类规范文档资源**
- `cpp-style://naming/{category}` - 命名规范
- `cpp-style://best-practices/{topic}` - 最佳实践
- `cpp-style://standard/{version}` - C++ 标准特性
- `cpp-style://examples/{pattern}` - 设计模式示例

**2 个代码审查提示模板**
- `code_review` - 综合/性能/安全/可读性审查
- `refactor_suggestion` - 重构建议

## 快速开始

### 通过 Smithery 安装（推荐）

```bash
npx -y @smithery/cli install cpp-style-guide-mcp --client claude
```

### 本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/lv5railgun/cpp_guidelines.git
cd cpp_guidelines

# 2. 安装依赖
uv sync

# 3. 添加到 Claude Desktop 配置
# 在 .mcp.json 或 Claude 配置文件中：
{
  "mcpServers": {
    "cpp-style": {
      "command": "uv",
      "args": ["run", "mcp", "run", "cpp_style_server.py"],
      "cwd": "/path/to/cpp_guidelines"
    }
  }
}
```

## 使用示例

```python
# 检查命名规范
请使用 check_naming 工具检查 "myVariable" 是否符合成员变量命名规范

# 分析内存安全
请分析以下代码的内存安全问题：
void processData(int* ptr) {
    delete ptr;
    ptr->process();  // 悬空指针！
}

# 现代化建议
请使用 suggest_modern_cpp 工具将代码升级到 C++17

# 查看文档
请获取资源 cpp-style://naming/all
请获取资源 cpp-style://best-practices/memory
```

## 发布到 Smithery

### 准备工作

项目已包含所有必需的配置文件：
- ✅ `smithery.yaml` - Smithery 部署配置
- ✅ `Dockerfile` - 容器化配置
- ✅ `pyproject.toml` - 项目元数据

### 发布步骤

```bash
# 1. 提交代码
git add .
git commit -m "准备发布到 Smithery"
git push origin main

# 2. 访问 Smithery 发布页面
# https://smithery.ai/new
# 连接 GitHub 仓库，Smithery 会自动检测配置并部署

# 3. 测试安装
npx -y @smithery/cli install cpp-style-guide-mcp --client claude
```

### 验证清单

- [ ] 本地测试通过: `uv run mcp run cpp_style_server.py`
- [ ] GitHub 仓库已推送
- [ ] Smithery 构建成功
- [ ] 可以通过 Smithery CLI 安装
- [ ] 工具调用正常

## 项目结构

```
cpp_guidelines/
├── cpp_style_server.py      # MCP 服务器主文件
├── cpp_style/               # 核心功能模块
│   ├── tools/              # 5个分析工具
│   └── resources/          # 4类规范文档
├── smithery.yaml           # Smithery 配置
├── Dockerfile              # 容器配置
└── pyproject.toml          # 项目元数据
```

## 开发

```bash
# 运行服务器
uv run mcp run cpp_style_server.py

# 添加新工具
@mcp.tool()
def your_tool(param: str) -> str:
    """工具描述"""
    return "result"

# 添加新资源
@mcp.resource("cpp-style://category/{param}")
def your_resource(param: str) -> str:
    return "content"
```

## 技术栈

- Python >= 3.12
- FastMCP >= 1.21.0
- uv (包管理)
- Docker (部署)

## 许可证

MIT License

## 链接

- GitHub: https://github.com/lv5railgun/cpp_guidelines
- Issues: https://github.com/lv5railgun/cpp_guidelines/issues
- Smithery: https://smithery.ai/