# 🚀 快速开始指南

只需 3 步，立即开始使用 C++ 编码规范 MCP 服务器！

## 方式 1: 自动安装（推荐）⚡

```bash
# 1. 进入项目目录
cd /home/lv5railgun/code/mcp_server_demo

# 2. 运行安装脚本
./install.sh

# 3. 验证安装
claude mcp list
```

**就这么简单！** 🎉

---

## 方式 2: 手动安装 🔧

### Step 1: 安装依赖

```bash
cd /home/lv5railgun/code/mcp_server_demo
uv sync
```

### Step 2: 添加到 Claude Code

```bash
claude mcp add --transport stdio cpp-style -- uv run mcp run cpp_style_server.py
```

### Step 3: 验证

```bash
claude mcp list
```

---

## 立即开始使用 💡

打开 Claude Code，试试这些命令：

### 1. 命名检查

```
请检查变量名 userName 是否符合 C++ 规范
```

### 2. 内存安全分析

```
请分析这段代码的内存安全问题：

Widget* w = new Widget();
char buffer[100];
strcpy(buffer, input);
delete w;
```

### 3. 现代 C++ 建议

```
请帮我将这段代码升级到 C++17：

int* ptr = NULL;
typedef std::vector<int> IntVec;
for (auto it = vec.begin(); it != vec.end(); ++it) {
    process(*it);
}
```

### 4. 查询 C++ 特性

```
C++17 有哪些主要特性？
```

### 5. 设计模式

```
如何用现代 C++ 实现线程安全的单例模式？
```

### 6. 最佳实践

```
C++ 内存管理有哪些最佳实践？
```

---

## 功能一览 📋

### 🛠️ 5个强大工具

1. **check_naming** - 命名规范检查
2. **check_include_guard** - 头文件保护检查
3. **analyze_memory_safety** - 内存安全分析
4. **suggest_modern_cpp** - 现代化建议
5. **check_const_correctness** - const 正确性检查

### 📚 4类丰富资源

1. **cpp-style://naming/{category}** - 8类命名规范
2. **cpp-style://best-practices/{topic}** - 6大主题最佳实践
3. **cpp-style://standard/{version}** - C++11~23 标准特性
4. **cpp-style://examples/{pattern}** - 6种设计模式

### 💡 2个提示模板

1. **code_review** - 代码审查提示
2. **refactor_suggestion** - 重构建议提示

---

## 网络模式（团队共享）🌐

### 启动服务器

```bash
# 方式 1: 使用安装脚本
./install.sh sse

# 方式 2: 手动启动
uv run mcp run cpp_style_server.py --transport sse --host 0.0.0.0 --port 8000
```

### 客户端连接

```bash
# 替换 <SERVER_IP> 为服务器 IP
claude mcp add --transport sse cpp-style http://<SERVER_IP>:8000/sse

# 示例（本地）
claude mcp add --transport sse cpp-style http://localhost:8000/sse
```

---

## 常见问题 ❓

### Q: 如何卸载？

```bash
claude mcp remove cpp-style
```

### Q: 如何更新？

```bash
cd /home/lv5railgun/code/mcp_server_demo
git pull  # 如果使用 git
uv sync
claude mcp remove cpp-style
./install.sh
```

### Q: 服务器无法启动？

```bash
# 检查 Python 版本
python3 --version  # 需要 >= 3.12

# 重新安装依赖
uv sync --reinstall

# 手动测试
uv run python cpp_style_server.py
```

### Q: 功能不完整？

```bash
# 验证所有模块
uv run python -c "from cpp_style_server import mcp; print('工具:', len(mcp._tool_manager._tools), '资源:', len(mcp._resource_manager._templates))"
# 应该输出: 工具: 5 资源: 4
```

---

## 更多文档 📖

- **完整功能文档**: [README_CPP_STYLE.md](./README_CPP_STYLE.md)
- **详细安装指南**: [INSTALL_CPP_STYLE.md](./INSTALL_CPP_STYLE.md)
- **开发指南**: [CLAUDE.md](./CLAUDE.md)

---

## 使用技巧 💡

### 直接提问

```
变量命名用什么风格？
C++20 有哪些新特性？
如何实现 RAII？
什么是 Pimpl 惯用法？
```

### 代码分析

```
[粘贴你的代码]
请分析这段代码的：
1. 内存安全问题
2. const 正确性
3. 现代化建议
```

### 学习参考

```
给我展示观察者模式的完整实现
C++ 异常处理最佳实践是什么？
如何正确使用智能指针？
```

---

**开始你的 C++ 编码之旅！** 🎊
