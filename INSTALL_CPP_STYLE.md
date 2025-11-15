# C++ 编码规范 MCP 服务器 - 安装和部署指南

## 📦 快速安装

### 方法 1: Claude Code 本地安装（推荐）

**适用场景**: 本地开发使用

```bash
# 进入项目目录
cd /home/lv5railgun/code/mcp_server_demo

# 添加 MCP 服务器到 Claude Code (stdio 模式)
claude mcp add --transport stdio cpp-style -- uv run mcp run cpp_style_server.py
```

**验证安装**:
```bash
# 查看已安装的 MCP 服务器
claude mcp list

# 应该能看到 cpp-style 服务器
```

**在 Claude Code 中使用**:
打开 Claude Code，输入 `/mcp` 查看可用服务器，或直接开始使用：
```
请检查这个变量名是否符合 C++ 规范：userName
```

---

### 方法 2: 网络模式部署（团队共享）

**适用场景**: 团队内多人使用，或远程访问

#### Step 1: 启动服务器

```bash
# 本地网络（局域网）
uv run mcp run cpp_style_server.py --transport sse --host 0.0.0.0 --port 8000

# 仅本机访问
uv run mcp run cpp_style_server.py --transport sse --port 8000
```

服务器启动后会显示：
```
Server running on http://0.0.0.0:8000
SSE endpoint: http://0.0.0.0:8000/sse
```

#### Step 2: 客户端连接

在其他机器上（或同一机器）：

```bash
# 替换 <SERVER_IP> 为服务器的 IP 地址
claude mcp add --transport sse cpp-style http://<SERVER_IP>:8000/sse

# 本地连接示例
claude mcp add --transport sse cpp-style http://localhost:8000/sse

# 局域网连接示例
claude mcp add --transport sse cpp-style http://192.168.1.100:8000/sse
```

#### Step 3: 保持服务器运行（可选）

使用 systemd 或 screen/tmux 保持服务器后台运行：

```bash
# 使用 screen
screen -S cpp-style-mcp
uv run mcp run cpp_style_server.py --transport sse --host 0.0.0.0 --port 8000
# 按 Ctrl+A, D 分离会话

# 重新连接
screen -r cpp-style-mcp
```

---

## 🧪 验证安装

### 测试工具功能

在 Claude Code 中尝试以下命令：

```
1. 测试命名检查：
   请检查变量名 userName 是否符合 C++ 规范

2. 测试内存安全分析：
   请分析以下代码的内存安全问题：
   Widget* w = new Widget();
   delete w;

3. 测试现代 C++ 建议：
   请帮我将以下代码升级到 C++17：
   int* ptr = NULL;
```

### 测试资源访问

```
1. 查看 C++17 特性：
   C++17 有哪些主要特性？

2. 查看单例模式实现：
   如何用现代 C++ 实现线程安全的单例模式？

3. 查看内存管理最佳实践：
   C++ 内存管理有哪些最佳实践？
```

---

## 🔧 配置选项

### 环境变量（可选）

```bash
# 设置日志级别
export MCP_LOG_LEVEL=debug

# 自定义端口
export MCP_PORT=9000
```

### 项目配置文件 `.mcp.json`

如果你想让项目自动提供 MCP 配置，创建 `.mcp.json`:

```json
{
  "mcpServers": {
    "cpp-style": {
      "command": "uv",
      "args": ["run", "mcp", "run", "cpp_style_server.py"],
      "cwd": "/home/lv5railgun/code/mcp_server_demo"
    }
  }
}
```

团队成员克隆项目后，Claude Code 会自动识别这个配置。

---

## 🌐 网络部署高级配置

### 使用反向代理（Nginx）

**适用场景**: 生产环境，需要 HTTPS 或负载均衡

#### Nginx 配置示例

```nginx
server {
    listen 443 ssl;
    server_name cpp-style.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /sse {
        proxy_pass http://localhost:8000/sse;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;
    }
}
```

客户端连接：
```bash
claude mcp add --transport sse cpp-style https://cpp-style.example.com/sse
```

### 使用 Docker（可选）

创建 `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "mcp", "run", "cpp_style_server.py", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：
```bash
docker build -t cpp-style-mcp .
docker run -d -p 8000:8000 cpp-style-mcp
```

---

## 🔐 安全建议

1. **本地使用**: 优先使用 stdio 模式，更安全
2. **网络模式**:
   - 仅在可信网络中使用
   - 使用防火墙限制访问
   - 考虑添加身份认证（需要自定义）
3. **生产环境**:
   - 使用 HTTPS
   - 实施访问控制
   - 定期更新依赖

---

## 📝 卸载

### 从 Claude Code 移除

```bash
claude mcp remove cpp-style
```

### 完全清理

```bash
# 移除 MCP 配置
claude mcp remove cpp-style

# 删除项目（如果不再需要）
rm -rf /home/lv5railgun/code/mcp_server_demo
```

---

## 🐛 故障排查

### 问题 1: 服务器无法启动

**检查**:
```bash
# 验证 Python 版本
python --version  # 应该 >= 3.12

# 验证依赖
uv sync

# 手动运行
uv run python cpp_style_server.py
```

### 问题 2: Claude Code 无法连接

**检查**:
```bash
# 确认服务器正在运行
curl http://localhost:8000/sse

# 查看 MCP 列表
claude mcp list

# 重新添加
claude mcp remove cpp-style
claude mcp add --transport stdio cpp-style -- uv run mcp run cpp_style_server.py
```

### 问题 3: 网络模式连接失败

**检查**:
```bash
# 测试网络连接
ping <SERVER_IP>

# 检查端口是否开放
telnet <SERVER_IP> 8000

# 检查防火墙
sudo ufw status
sudo ufw allow 8000
```

### 问题 4: 功能不完整

**检查**:
```bash
# 验证所有模块
uv run python -c "from cpp_style_server import mcp; print(len(mcp._tool_manager._tools))"
# 应该输出: 5

# 重新安装依赖
uv sync --reinstall
```

---

## 💡 使用技巧

### 1. 快速查询

```
# 命名规范
变量应该用什么命名风格？

# 标准特性
C++20 有哪些新特性？

# 设计模式
如何实现 RAII？
```

### 2. 代码检查

```
# 贴上代码，然后：
请检查这段代码的内存安全问题
请分析这段代码的 const 正确性
请建议如何现代化这段代码
```

### 3. 学习和参考

```
请给我展示工厂模式的现代 C++ 实现
C++ 异常处理有哪些最佳实践？
如何正确使用智能指针？
```

---

## 📚 更多资源

- 完整文档: [README_CPP_STYLE.md](./README_CPP_STYLE.md)
- 项目指南: [CLAUDE.md](./CLAUDE.md)
- MCP 协议: https://modelcontextprotocol.io/

---

## 🆘 获取帮助

如有问题：
1. 查看 [README_CPP_STYLE.md](./README_CPP_STYLE.md) 中的常见问题
2. 运行 `claude mcp list` 检查安装状态
3. 在项目 Issues 中提问

---

**祝你使用愉快！** 🎉
