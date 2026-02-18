# 多阶段构建 - 构建阶段
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# 从 uv 镜像复制 uv 二进制文件
COPY --from=ghcr.io/astral-sh/uv:0.5.16 /uv /bin/uv

# 复制项目文件
COPY . .

# 安装依赖
RUN if [ -f "uv.lock" ]; then \
      echo "Using uv with uv.lock" && \
      export UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy && \
      uv sync --frozen --no-dev; \
    elif [ -f "poetry.lock" ]; then \
      echo "Using poetry with poetry.lock" && \
      pip install poetry && \
      poetry install --no-dev; \
    else \
      echo "Using uv with pyproject.toml" && \
      export UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy && \
      uv sync --no-dev; \
    fi

# 运行时阶段
FROM python:3.12-slim-bookworm

WORKDIR /app

# 从构建阶段复制应用和虚拟环境
COPY --from=builder /app /app

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV MCP_TRANSPORT=streamable-http

# PORT 由部署平台通过环境变量注入（Fly.io 默认 8080）
EXPOSE ${PORT:-8080}

# 启动 MCP 服务器
CMD ["python", "cpp_style_server.py"]
