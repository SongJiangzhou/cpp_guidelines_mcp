# 多阶段构建 - 构建阶段
FROM ghcr.io/astral-sh/uv:0.5.16 AS builder

WORKDIR /app

# 复制项目文件
COPY . .

# 复制 uv 到构建器
COPY --from=ghcr.io/astral-sh/uv:0.5.16 /uv /bin/uv

# 安装依赖
RUN if [ -f "uv.lock" ]; then \
      echo "Using uv with uv.lock" && \
      export UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy && \
      uv sync --frozen --no-dev; \
    elif [ -f "poetry.lock" ]; then \
      echo "Using poetry with poetry.lock" && \
      export PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1 \
        PIP_NO_CACHE_DIR=off \
        PIP_DISABLE_PIP_VERSION_CHECK=on \
        POETRY_HOME="/opt/poetry" \
        POETRY_VIRTUALENVS_IN_PROJECT=true \
        POETRY_NO_INTERACTION=1 && \
      export PATH="$POETRY_HOME/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" && \
      pip install poetry && \
      poetry install --no-dev; \
    else \
      echo "Using uv with pyproject.toml" && \
      export UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy && \
      uv sync --no-dev; \
    fi

# 运行时阶段
FROM python:3.12-slim-bookworm AS base

WORKDIR /app

# 从构建阶段复制应用
COPY --from=builder /app /app

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV MCP_TRANSPORT=streamable-http

# Smithery 会设置 PORT 环境变量
EXPOSE ${PORT:-8000}

# 启动 MCP 服务器
CMD ["python", "cpp_style_server.py"]
