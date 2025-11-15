#!/bin/bash

# C++ 编码规范 MCP 服务器 - 快速安装脚本
# 使用方法: ./install.sh [stdio|sse]

set -e

echo "============================================================"
echo "  C++ 编码规范 MCP 服务器 - 安装程序"
echo "============================================================"
echo

# 检查 Python 版本
check_python() {
    echo "📌 检查 Python 版本..."
    if ! command -v python3 &> /dev/null; then
        echo "❌ 错误: 未找到 Python 3"
        exit 1
    fi

    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version="3.12"

    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        echo "❌ 错误: 需要 Python >= 3.12，当前版本: $python_version"
        exit 1
    fi

    echo "✅ Python 版本: $python_version"
}

# 检查 uv
check_uv() {
    echo "📌 检查 uv 包管理器..."
    if ! command -v uv &> /dev/null; then
        echo "⚠️  未找到 uv，正在安装..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    echo "✅ uv 已安装"
}

# 检查 Claude Code
check_claude() {
    echo "📌 检查 Claude Code..."
    if ! command -v claude &> /dev/null; then
        echo "❌ 错误: 未找到 Claude Code CLI"
        echo "请先安装 Claude Code: https://claude.com/claude-code"
        exit 1
    fi
    echo "✅ Claude Code 已安装"
}

# 安装依赖
install_deps() {
    echo "📌 安装项目依赖..."
    uv sync
    echo "✅ 依赖安装完成"
}

# 测试服务器
test_server() {
    echo "📌 测试服务器功能..."
    uv run python -c "
from cpp_style_server import mcp
tools = len(mcp._tool_manager._tools)
resources = len(mcp._resource_manager._templates)
prompts = len(mcp._prompt_manager._prompts)
print(f'  ✓ 工具: {tools}')
print(f'  ✓ 资源: {resources}')
print(f'  ✓ 提示: {prompts}')
assert tools == 5, '工具数量不正确'
assert resources == 4, '资源数量不正确'
assert prompts == 2, '提示数量不正确'
"
    echo "✅ 服务器功能测试通过"
}

# 安装到 Claude Code (stdio 模式)
install_stdio() {
    echo "📌 安装到 Claude Code (stdio 模式)..."

    # 获取项目绝对路径
    project_dir=$(pwd)

    # 移除旧配置（如果存在）
    claude mcp remove cpp-style 2>/dev/null || true

    # 添加新配置
    cd "$project_dir"
    claude mcp add --transport stdio cpp-style -- uv run mcp run cpp_style_server.py

    echo "✅ stdio 模式安装完成"
}

# 启动网络服务器 (SSE 模式)
start_sse_server() {
    echo "📌 启动网络服务器 (SSE 模式)..."
    echo
    echo "服务器将在以下地址启动:"
    echo "  本地访问: http://localhost:8000/sse"
    echo "  局域网访问: http://$(hostname -I | awk '{print $1}'):8000/sse"
    echo
    echo "按 Ctrl+C 停止服务器"
    echo

    uv run mcp run cpp_style_server.py --transport sse --host 0.0.0.0 --port 8000
}

# 显示使用说明
show_usage() {
    echo
    echo "============================================================"
    echo "  ✅ 安装完成！"
    echo "============================================================"
    echo
    echo "🎯 验证安装:"
    echo "  claude mcp list"
    echo
    echo "💡 使用示例:"
    echo "  打开 Claude Code，输入:"
    echo "  \"请检查变量名 userName 是否符合 C++ 规范\""
    echo
    echo "📚 查看完整文档:"
    echo "  cat README_CPP_STYLE.md"
    echo "  cat INSTALL_CPP_STYLE.md"
    echo
    echo "🆘 获取帮助:"
    echo "  /mcp (在 Claude Code 中查看 MCP 服务器)"
    echo
}

# 主流程
main() {
    # 解析参数
    mode=${1:-stdio}

    if [ "$mode" != "stdio" ] && [ "$mode" != "sse" ]; then
        echo "用法: $0 [stdio|sse]"
        echo
        echo "  stdio - 本地模式（推荐）"
        echo "  sse   - 网络模式（团队共享）"
        exit 1
    fi

    # 执行检查
    check_python
    check_uv
    install_deps
    test_server

    if [ "$mode" = "stdio" ]; then
        check_claude
        install_stdio
        show_usage
    else
        echo
        echo "============================================================"
        echo "  网络模式启动"
        echo "============================================================"
        echo
        echo "在其他机器上运行以下命令连接:"
        echo "  claude mcp add --transport sse cpp-style http://<SERVER_IP>:8000/sse"
        echo
        start_sse_server
    fi
}

# 运行主流程
main "$@"
