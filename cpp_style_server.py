"""
C++ 编码规范 MCP 服务器

提供 C++ 代码规范检查、最佳实践建议和代码审查支持。
"""

import os
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, RedirectResponse

# 导入工具模块
from cpp_style.tools.naming_checker import get_checker as get_naming_checker
from cpp_style.tools.include_guard_checker import get_checker as get_include_guard_checker
from cpp_style.tools.memory_safety import get_analyzer as get_memory_analyzer
from cpp_style.tools.modern_cpp import get_suggester as get_modern_cpp_suggester
from cpp_style.tools.const_checker import get_checker as get_const_checker

# 导入资源模块
from cpp_style.resources.naming_rules import get_resource as get_naming_resource
from cpp_style.resources.best_practices import get_resource as get_practices_resource
from cpp_style.resources.cpp_standards import get_resource as get_standards_resource
from cpp_style.resources.design_patterns import get_resource as get_patterns_resource

# 导入提示模块
from cpp_style.prompts.code_review import get_prompt as get_code_review_prompt
from cpp_style.prompts.refactor_suggestion import get_prompt as get_refactor_prompt

# ==================== OAuth 配置 ====================

# GitHub OAuth 环境变量（在 Railway 中配置）
_GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
_GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
# MCP 服务器公开 URL（Railway 部署地址或自定义域名）
_MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "https://cpp-style-guide-mcp.fly.dev",
)

_oauth_provider = None
_auth_settings = None

if _GITHUB_CLIENT_ID and _GITHUB_CLIENT_SECRET:
    from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions
    from mcp.server.auth.provider import ProviderTokenVerifier
    from cpp_style.auth.github_provider import GitHubOAuthProvider

    _oauth_provider = GitHubOAuthProvider(
        github_client_id=_GITHUB_CLIENT_ID,
        github_client_secret=_GITHUB_CLIENT_SECRET,
        mcp_server_url=_MCP_SERVER_URL,
    )
    _auth_settings = AuthSettings(
        issuer_url=_MCP_SERVER_URL,  # type: ignore[arg-type]
        resource_server_url=_MCP_SERVER_URL,  # type: ignore[arg-type]
        client_registration_options=ClientRegistrationOptions(
            enabled=True,
            valid_scopes=["mcp"],
            default_scopes=["mcp"],
        ),
    )

# 创建 MCP 服务器实例
# stateless_http=True：每个请求独立处理，无需 session ID
# 使 Smithery 扫描器可以直接查询 tools/list 等端点
mcp = FastMCP(
    "C++ Style Guide Server",
    auth_server_provider=_oauth_provider,
    token_verifier=ProviderTokenVerifier(_oauth_provider) if _oauth_provider else None,
    auth=_auth_settings,
    stateless_http=True,
)


# ==================== Custom Routes ====================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """健康检查端点（供 Railway 等平台使用）"""
    auth_enabled = _oauth_provider is not None
    return JSONResponse({
        "status": "ok",
        "service": "cpp-style-guide-mcp",
        "auth": "github" if auth_enabled else "disabled",
    })


@mcp.custom_route("/.well-known/mcp/server-card.json", methods=["GET"])
async def server_card(request: Request) -> FileResponse | JSONResponse:
    """Smithery 服务器元数据（用于 Smithery 平台展示）"""
    card_path = Path(__file__).parent / "static" / ".well-known" / "mcp" / "server-card.json"
    if card_path.exists():
        return FileResponse(str(card_path), media_type="application/json")
    return JSONResponse({"error": "server-card.json 未找到"}, status_code=404)


@mcp.custom_route("/oauth/callback", methods=["GET"])
async def oauth_callback(request: Request) -> RedirectResponse | JSONResponse:
    """GitHub OAuth 回调处理（GitHub 授权后重定向到此路由）"""
    if _oauth_provider is None:
        return JSONResponse({"error": "OAuth 未启用"}, status_code=400)

    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        return JSONResponse({"error": "缺少 code 或 state 参数"}, status_code=400)

    try:
        redirect_url = await _oauth_provider.handle_github_callback(code, state)
        return RedirectResponse(url=redirect_url, status_code=302)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


# ==================== Tools ====================

_READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)


@mcp.tool(
    description="Check whether a C++ identifier follows naming conventions. Validates variables, constants, functions, classes, namespaces, member variables, template parameters, and file names against established C++ style guidelines. Returns whether the identifier is valid, a detailed explanation, and suggested alternatives if it violates the rules.",
    annotations=_READ_ONLY,
)
def check_naming(
    identifier: str,
    category: Literal["variable", "constant", "function", "class", "namespace", "member_variable", "template_parameter", "file_naming"],
) -> str:
    """
    检查 C++ 标识符命名是否符合规范

    参数:
        identifier: 要检查的标识符名称
        category: 标识符类别（variable/constant/function/class/namespace/member_variable/template_parameter/file_naming）

    返回:
        检查结果，包含是否符合规范、详细说明和建议
    """
    checker = get_naming_checker()
    is_valid, details, suggestions = checker.check_naming(identifier, category)

    result = details
    if suggestions:
        result += f"\n推荐使用:\n"
        for sug in suggestions:
            result += f"  • {sug}\n"

    return result


@mcp.tool(
    description="Check whether a C++ header file has correct include guards or #pragma once directives. Detects missing guards, malformed macro names, mismatched #endif comments, and suggests correctly formatted guard macros based on the file path.",
    annotations=_READ_ONLY,
)
def check_include_guard(code: str, file_path: str = "") -> str:
    """
    检查 C++ 头文件的包含保护是否正确

    参数:
        code: 头文件的完整代码
        file_path: 可选的文件路径，用于生成建议的保护宏名

    返回:
        检查结果，包含是否符合规范、详细说明和建议
    """
    checker = get_include_guard_checker()

    file_path_param = file_path if file_path else None
    is_valid, details, suggestions = checker.check_include_guard(code, file_path_param)

    result = details
    if suggestions and not is_valid:
        result += f"\n建议的保护宏名:\n"
        for sug in suggestions:
            result += f"  • {sug}\n"

    return result


@mcp.tool(
    description="Analyze C++ code for memory safety issues including memory leaks, dangling pointers, double-free errors, use of raw owning pointers, missing RAII patterns, and unsafe array operations. Returns a detailed report with line-level findings and recommendations to use modern C++ alternatives like smart pointers.",
    annotations=_READ_ONLY,
)
def analyze_memory_safety(code: str) -> str:
    """
    分析 C++ 代码中的内存安全问题

    参数:
        code: 要分析的 C++ 代码

    返回:
        内存安全分析报告，包括潜在的内存泄漏、悬空指针、不安全操作等
    """
    analyzer = get_memory_analyzer()
    issues, report = analyzer.analyze_memory_safety(code)
    return report


@mcp.tool(
    description="Suggest how to modernize C++ code to use features from a target standard (C++11 through C++23). Identifies outdated patterns such as raw loops replaceable by range-for, C-style casts, manual memory management, pre-C++11 type aliases, and suggests concrete rewrites using modern idioms like auto, structured bindings, std::optional, concepts, and ranges.",
    annotations=_READ_ONLY,
)
def suggest_modern_cpp(
    code: str,
    target_standard: Literal["cpp11", "cpp14", "cpp17", "cpp20", "cpp23"] = "cpp17",
) -> str:
    """
    建议将代码升级为现代 C++ 写法

    参数:
        code: 要分析的 C++ 代码
        target_standard: 目标 C++ 标准（cpp11/cpp14/cpp17/cpp20/cpp23，默认 cpp17）

    返回:
        现代化建议报告，包括可以使用的新特性和重写示例
    """
    suggester = get_modern_cpp_suggester()
    suggestions, report = suggester.suggest_modern_cpp(code, target_standard)
    return report


@mcp.tool(
    description="Check C++ code for const correctness issues. Identifies member functions that do not modify state but are missing the const qualifier, non-const references where const references would suffice, and variables that are never modified but not declared const. Returns a report with specific locations and suggested fixes.",
    annotations=_READ_ONLY,
)
def check_const_correctness(code: str) -> str:
    """
    检查 C++ 代码中的 const 正确性

    参数:
        code: 要检查的 C++ 代码

    返回:
        const 正确性检查报告，包括缺少 const 的地方和改进建议
    """
    checker = get_const_checker()
    issues, report = checker.check_const_correctness(code)
    return report


# ==================== Resources ====================

@mcp.resource("cpp-style://naming/{category}")
def get_naming_convention(category: str) -> str:
    """
    获取 C++ 命名规范文档

    可用的类别:
    - variable: 变量命名
    - constant: 常量命名
    - function: 函数命名
    - class: 类命名
    - namespace: 命名空间命名
    - member_variable: 成员变量命名
    - template_parameter: 模板参数命名
    - file_naming: 文件命名
    - all: 查看所有类别
    """
    resource = get_naming_resource()

    if category == "all":
        return resource.get_all_categories()

    return resource.get_naming_rule(category)


@mcp.resource("cpp-style://best-practices/{topic}")
def get_best_practice(topic: str) -> str:
    """
    获取 C++ 最佳实践指南

    可用的主题:
    - memory: 内存管理
    - exceptions: 异常处理
    - templates: 模板编程
    - concurrency: 并发编程
    - performance: 性能优化
    - modern_cpp: 现代 C++ 特性
    - all: 查看所有主题
    """
    resource = get_practices_resource()

    if topic == "all":
        return resource.get_all_topics()

    return resource.get_best_practice(topic)


@mcp.resource("cpp-style://standard/{version}")
def get_cpp_standard(version: str) -> str:
    """
    获取 C++ 标准特性文档

    可用的版本:
    - cpp11: C++11 特性
    - cpp14: C++14 特性
    - cpp17: C++17 特性
    - cpp20: C++20 特性
    - cpp23: C++23 特性
    - all: 查看所有标准概览
    """
    resource = get_standards_resource()

    if version == "all":
        return resource.get_all_standards()

    return resource.get_standard_features(version)


@mcp.resource("cpp-style://examples/{pattern}")
def get_design_pattern(pattern: str) -> str:
    """
    获取 C++ 设计模式示例

    可用的模式:
    - singleton: 单例模式
    - factory: 工厂模式
    - observer: 观察者模式
    - raii: RAII 惯用法
    - pimpl: Pimpl 惯用法
    - strategy: 策略模式
    - all: 查看所有模式
    """
    resource = get_patterns_resource()

    if pattern == "all":
        return resource.get_all_patterns()

    return resource.get_pattern_example(pattern)


# ==================== Prompts ====================

@mcp.prompt()
def code_review(focus: str = "general") -> str:
    """
    生成 C++ 代码审查提示模板

    参数:
        focus: 审查重点，可选值:
              - general: 综合审查（默认）
              - performance: 性能优化
              - safety: 内存和类型安全
              - readability: 可读性和维护性
              - modern: 现代 C++ 特性使用
    """
    prompt_generator = get_code_review_prompt()
    return prompt_generator.generate(focus)


@mcp.prompt()
def refactor_suggestion(target_standard: str = "cpp17") -> str:
    """
    生成代码重构建议提示模板

    参数:
        target_standard: 目标 C++ 标准
                        - cpp11: C++11
                        - cpp14: C++14
                        - cpp17: C++17
                        - cpp20: C++20
                        - cpp23: C++23
    """
    prompt_generator = get_refactor_prompt()
    return prompt_generator.generate(target_standard)


# 启动服务器（仅在直接运行时）
if __name__ == "__main__":
    # 从环境变量检测运行模式，默认为 stdio
    # Smithery 部署时使用 streamable-http，本地开发使用 stdio
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        # HTTP 模式：使用 uvicorn 手动启动以支持 PORT 环境变量
        import uvicorn

        port = int(os.environ.get("PORT", "8000"))

        # 获取 FastMCP 的 streamable HTTP 应用（已包含 /health 自定义路由）
        app = mcp.streamable_http_app()

        # 启动服务器
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # stdio 模式：使用标准方式启动
        mcp.run(transport=transport)
