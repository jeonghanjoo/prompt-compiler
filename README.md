# Prompt Compiler

A tool for generating code from prompt files using AI models (GPT, Claude, etc.). It automatically generates both source code and test code based on the given prompts.

## Features

- Prompt-based code generation
- Automatic test code generation
- Multiple AI model support (GPT, Claude)
- Response caching system
- Code formatting and validation
- Rate limiting handling
- CLI interface

## Installation

```bash
poetry install
```

## CLI Usage

### Basic Usage

```bash
# Compile single file
prompt-compiler input.prompt

# Compile multiple files
prompt-compiler input1.prompt input2.prompt

# Specify output directory
prompt-compiler input.prompt -o generated/
```

### Configuration File

Use `prompt-compiler.yaml` to specify default settings:

```yaml
# AI Model Configuration
api_key: "your-api-key-here"
model: "gpt"  # or "claude"
model_name: "gpt-4"  # or "gpt-3.5-turbo", "claude-3-opus-20240229", etc.

# Output Configuration
output_dir: "generated"
format: "split"  # or "single"

# Cache Configuration
cache_dir: ".cache"
```

### CLI Options

```bash
# Specify config file
prompt-compiler input.prompt -c my-config.yaml

# Directly specify API key
prompt-compiler input.prompt --api-key="your-key-here"

# Select AI model
prompt-compiler input.prompt --model=claude

# Specify model version
prompt-compiler input.prompt --model=gpt --model-name=gpt-4
prompt-compiler input.prompt --model=claude --model-name=claude-3-sonnet-20240229

# Force rebuild, ignore cache
prompt-compiler input.prompt --force

# Specify cache directory
prompt-compiler input.prompt --cache-dir=.my-cache

# Specify output format (single/split)
prompt-compiler input.prompt --format=single
```

## Writing Prompt Files

Create a `.prompt` file in the `prompts` directory:

```yaml
name: Example
description: A simple example function
template: |
  def hello_world():
      # TODO: Implement
      pass

requirements:
  - Print "Hello, World!"
  - Return None

language: python
```

## Programmatic Usage

```python
from pathlib import Path
from prompt_compiler.compiler import Compiler
from prompt_compiler.ai_adapters import GptAdapter

# Initialize AI adapter
adapter = GptAdapter(api_key="your-api-key")

# Initialize compiler
compiler = Compiler(adapter)

# Generate code from prompt
result = compiler.compile(Path("prompts/example.prompt"))

# Print generated code and tests
print("Generated Code:")
print(result["code"])
print("\nGenerated Tests:")
print(result["tests"])
```

## Advanced Features

### Using Cache

```python
compiler = Compiler(adapter, cache_dir=Path(".cache"))
result = compiler.compile(prompt_file, force_rebuild=False)  # Use cache
```

### Custom Formatter

```python
from prompt_compiler.formatters import CodeFormatter, ResponseProcessor

class CustomFormatter(CodeFormatter):
    def format(self, code: str) -> str:
        # Custom formatting logic
        return code

formatter = ResponseProcessor(CustomFormatter())
compiler = Compiler(adapter, formatter=formatter)
```

### Custom Template

```python
from prompt_compiler.templates import BaseTemplate

class CustomTemplate(BaseTemplate):
    def get_system_prompt(self) -> str:
        return "Custom system prompt..."

    def get_template(self) -> str:
        return "Custom template string..."

compiler = Compiler(adapter, template=CustomTemplate())
```

## Error Handling

```python
from prompt_compiler.exceptions import (
    PromptCompilerError,
    AIAdapterError,
    RateLimitError,
    ValidationError,
)

try:
    result = compiler.compile(prompt_file)
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Validation failed: {e}")
except AIAdapterError as e:
    print(f"AI model error: {e}")
```

## Development

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Sort imports: `poetry run isort .`
- Type check: `poetry run mypy .`

## License

MIT License

