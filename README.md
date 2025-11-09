# MCP Server Demo

这是一个使用 FastMCP 框架构建的 MCP (Model Context Protocol) 服务器演示项目。

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 运行服务器

**本地模式**:
```bash
uv run mcp run server.py
```

**网络模式** (供他人远程使用):
```bash
# 局域网访问
uv run mcp run server.py --transport sse --host 0.0.0.0 --port 8000

# 公网访问 (推荐使用 Cloudflare Tunnel)
cloudflared tunnel --url http://localhost:8000
```

### 3. 连接到服务器

**本地连接** (stdio 模式):
```bash
claude mcp add --transport stdio demo -- uv run mcp run server.py
```

**远程连接** (网络模式):
```bash
# 局域网
claude mcp add --transport sse demo http://192.168.1.100:8000/sse

# 公网 (Cloudflare Tunnel)
claude mcp add --transport sse demo https://xxx.trycloudflare.com/sse
```

**验证连接**:
```bash
claude mcp list
```

## 功能特性

这个 MCP 服务器提供了三种类型的组件示例：

### 🔧 工具 (Tools)
- **add**: 执行两个数字的加法运算

### 📦 资源 (Resources)
- **greeting://{name}**: 获取个性化问候语

### 💬 提示 (Prompts)
- **greet_user**: 生成不同风格的问候语（friendly、formal、casual）

## 项目结构

```
mcp-server-demo/
├── server.py           # MCP 服务器主文件
├── main.py            # 入口脚本
├── .mcp.json          # MCP 配置文件（团队共享）
├── pyproject.toml     # Python 项目配置
├── CLAUDE.md          # Claude Code 使用指南
└── MCP_USAGE.md       # .mcp.json 详细使用说明
```

## 网络分享配置

### 三种分享方式

| 方式 | 适用场景 | 命令 |
|------|----------|------|
| **局域网** | 团队内网 | `--host 0.0.0.0 --port 8000` |
| **Cloudflare Tunnel** | 公网访问(推荐) | `cloudflared tunnel --url http://localhost:8000` |
| **SSH 隧道** | 临时测试 | `ssh -L 8000:localhost:8000 user@server` |

### 安全建议

**生产环境必须启用认证**:
```bash
export MCP_AUTH_TOKEN="your-secret-token"
uv run mcp run server.py --transport sse --port 8000
```

客户端连接:
```bash
claude mcp add --transport sse demo http://server:8000/sse \
  --header "Authorization: Bearer your-secret-token"
```

### 测试连接

```bash
# 测试服务器运行状态
curl http://localhost:8000/health

# 测试 SSE 端点
curl -N http://localhost:8000/sse
```

## 文档

- **[CLAUDE.md](CLAUDE.md)** - 项目架构和开发命令
- **[MCP_USAGE.md](MCP_USAGE.md)** - .mcp.json 配置详细指南

## 环境变量

如果你的 MCP 服务器需要环境变量：

1. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入实际值

3. 在 `.mcp.json` 中使用 `${VAR_NAME}` 引用环境变量

详见 [MCP_USAGE.md](MCP_USAGE.md) 了解更多配置选项。

## 开发

### 添加新工具

```python
@mcp.tool()
def your_tool(param: str) -> str:
    """工具描述"""
    return "result"
```

### 添加新资源

```python
@mcp.resource("resource://{param}")
def your_resource(param: str) -> str:
    """资源描述"""
    return f"Resource content for {param}"
```

### 添加新提示

```python
@mcp.prompt()
def your_prompt(param: str) -> str:
    """提示描述"""
    return f"Prompt template for {param}"
```

## 技术栈

- **Python**: >= 3.12
- **FastMCP**: >= 1.21.0
- **包管理器**: uv

## 许可证

MIT
