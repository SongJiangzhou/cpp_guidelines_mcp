# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 MCP (Model Context Protocol) 服务器演示项目，使用 FastMCP 框架构建。MCP 是一个用于 AI 模型与外部工具、资源和提示交互的协议。

## 语言规范
- 所有对话和文档都使用中文
- 注释使用中文
- 错误提示使用中文
- 文档使用中文Markdown格式

## 核心架构

**server.py** - 主要的 MCP 服务器实现
- 使用 `FastMCP` 类创建 MCP 服务器实例
- 通过装饰器定义三种类型的 MCP 组件：
  - `@mcp.tool()`: 定义可调用的工具函数（示例：`add` 函数用于加法运算）
  - `@mcp.resource()`: 定义动态资源，支持 URI 模板（示例：`greeting://{name}`）
  - `@mcp.prompt()`: 定义提示模板，支持参数化生成（示例：`greet_user` 支持不同风格的问候）

**main.py** - 简单的入口脚本（当前仅包含演示代码）

## 开发命令

### 运行 MCP 服务器

**本地模式 (stdio)**:
```bash
uv run mcp run server.py
```

**网络模式 (SSE)**:
```bash
# 本地开发
uv run mcp run server.py --transport sse --port 8000

# 允许外部访问
uv run mcp run server.py --transport sse --host 0.0.0.0 --port 8000
```

详细的网络分享配置请参考 [README.md](./README.md#网络分享配置)

### 依赖管理
项目使用 `uv` 作为包管理器：
```bash
# 安装依赖
uv sync

# 添加新依赖
uv add <package-name>
```

## MCP 组件开发规范

当添加新的 MCP 功能时：

1. **工具 (Tools)**: 用于执行操作或计算
   - 必须包含清晰的文档字符串
   - 使用类型注解定义参数和返回值
   - 函数名应清晰描述功能

2. **资源 (Resources)**: 用于提供数据或内容
   - URI 模板使用 `{variable}` 语法
   - 资源应返回字符串内容
   - 适合提供动态生成的内容

3. **提示 (Prompts)**: 用于生成 AI 提示模板
   - 支持可选参数提供灵活性
   - 返回格式化的提示文本
   - 可包含预定义的样式或模式

## Python 版本

项目要求 Python >= 3.12

## 在 Claude Code 中安装此 MCP 服务器

### 本地安装（仅当前项目可用）

**stdio 模式**:
```bash
claude mcp add --transport stdio demo -- uv run mcp run server.py
```

**网络模式 (连接远程服务器)**:
```bash
# 连接到远程 MCP 服务器
claude mcp add --transport sse demo http://[服务器IP]:8000/sse

# 示例: 连接到本地网络服务器
claude mcp add --transport sse demo http://192.168.1.100:8000/sse
```

### 项目共享配置

项目已包含 `.mcp.json` 配置文件，团队成员可直接使用。配置会自动被 Claude Code 识别。

### 网络分享给他人使用

参考 [README.md 网络分享配置](./README.md#网络分享配置) 了解:
- 局域网/公网访问配置
- 安全认证设置
- 连接测试方法

### 验证安装

在 Claude Code 中运行：
```bash
claude mcp list
```

或在对话中使用：
```
/mcp
```

### 使用 MCP 工具

安装后，Claude Code 可以自动调用服务器提供的工具、资源和提示：
- **add** 工具：执行两数相加
- **greeting://{name}** 资源：获取个性化问候
- **greet_user** 提示：生成不同风格的问候语
