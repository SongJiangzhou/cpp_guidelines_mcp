# C++ Style Guide MCP Server

Enforce consistent C++ style and best practices across your codebase. Analyze naming conventions, memory safety, and const correctness, and get actionable modernization suggestions up to C++23. Accelerate reviews with ready-made prompts and quick access to curated guidelines.

## Tools

| Tool | Description |
|------|-------------|
| `check_naming` | Validate C++ identifiers (variables, classes, functions, etc.) against naming conventions |
| `check_include_guard` | Verify header file include guards or `#pragma once` usage |
| `analyze_memory_safety` | Detect memory leaks, dangling pointers, and unsafe memory patterns |
| `suggest_modern_cpp` | Get modernization suggestions targeting C++11 through C++23 |
| `check_const_correctness` | Find missing `const` qualifiers on member functions, parameters, and variables |

## Resources

| URI | Description |
|-----|-------------|
| `cpp-style://naming/{category}` | Naming convention reference (variable, class, function, namespace, …) |
| `cpp-style://best-practices/{topic}` | Best practice guides (memory, exceptions, templates, concurrency, …) |
| `cpp-style://standard/{version}` | C++ standard feature docs (cpp11 – cpp23) |
| `cpp-style://examples/{pattern}` | Design pattern examples (RAII, Pimpl, Factory, Observer, …) |

## Prompts

| Prompt | Description |
|--------|-------------|
| `code_review` | Code review template (general / performance / safety / readability / modern) |
| `refactor_suggestion` | Refactoring guide targeting a specific C++ standard |

## Usage

### Connect via Smithery (recommended)

```bash
npx -y @smithery/cli install @SongJiangzhou/cpp_guidelines --client claude
```

### MCP endpoint (HTTP / streamable-http)

```
https://cpp-style-guide-mcp.fly.dev/mcp
```

### Local installation

```bash
git clone https://github.com/SongJiangzhou/cpp_guidelines_mcp.git
cd cpp_guidelines_mcp
uv sync
uv run mcp run cpp_style_server.py
```

Add to your MCP client config:

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

## Examples

```
# Check a variable name
check_naming("myVariable", "variable")

# Analyze memory safety
analyze_memory_safety("void f(int* p) { delete p; p->run(); }")

# Modernize code to C++17
suggest_modern_cpp("for (int i=0; i<v.size(); i++) {...}", "cpp17")

# Check const correctness
check_const_correctness("class Foo { int getValue() { return x; } int x; };")

# Access naming convention docs
Resource: cpp-style://naming/all

# Access memory best practices
Resource: cpp-style://best-practices/memory
```

## Project Structure

```
cpp_guidelines_mcp/
├── cpp_style_server.py        # MCP server entry point
├── cpp_style/
│   ├── tools/                 # 5 analysis tools
│   ├── resources/             # 4 reference resource categories
│   ├── prompts/               # 2 prompt templates
│   └── data/                  # JSON knowledge base
├── fly.toml                   # Fly.io deployment config
├── Dockerfile                 # Container image
└── smithery.yaml              # Smithery config (local stdio mode)
```

## Tech Stack

- Python >= 3.12
- [FastMCP](https://github.com/jlowin/fastmcp) >= 1.21.0
- [uv](https://github.com/astral-sh/uv) package manager
- Deployed on [Fly.io](https://fly.io)

## License

[MIT](LICENSE)

## Links

- GitHub: https://github.com/SongJiangzhou/cpp_guidelines_mcp
- Issues: https://github.com/SongJiangzhou/cpp_guidelines_mcp/issues
- Smithery: https://smithery.ai/server/SongJiangzhou/cpp_guidelines
