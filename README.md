# Prompt Compiler

프롬프트 파일을 기반으로 코드를 생성하는 도구입니다. AI 모델(GPT, Claude 등)을 활용하여 프롬프트로부터 코드와 테스트를 자동으로 생성합니다.

## 주요 기능

- 프롬프트 기반 코드 생성
- 자동 테스트 코드 생성
- 다양한 AI 모델 지원 (GPT, Claude)
- 응답 캐싱 시스템
- 코드 포맷팅 및 검증
- 레이트 리미팅 처리
- CLI 인터페이스

## 설치

```bash
poetry install
```

## CLI 사용법

### 기본 사용법

```bash
# 단일 파일 컴파일
prompt-compiler input.prompt

# 여러 파일 컴파일
prompt-compiler input1.prompt input2.prompt

# 출력 디렉토리 지정
prompt-compiler input.prompt -o generated/
```

### 설정 파일

`prompt-compiler.yaml` 파일을 사용하여 기본 설정을 지정할 수 있습니다:

```yaml
# AI Model Configuration
api_key: "your-api-key-here"
model: "gpt"  # or "claude"

# Output Configuration
output_dir: "generated"
format: "split"  # or "single"

# Cache Configuration
cache_dir: ".cache"
```

### CLI 옵션

```bash
# 설정 파일 지정
prompt-compiler input.prompt -c my-config.yaml

# API 키 직접 지정
prompt-compiler input.prompt --api-key="your-key-here"

# AI 모델 선택
prompt-compiler input.prompt --model=claude

# 특정 모델 버전 지정
prompt-compiler input.prompt --model=gpt --model-name=gpt-4
prompt-compiler input.prompt --model=claude --model-name=claude-3-sonnet-20240229

# 캐시 무시하고 강제 재생성
prompt-compiler input.prompt --force

# 캐시 디렉토리 지정
prompt-compiler input.prompt --cache-dir=.my-cache

# 출력 형식 지정 (단일/분할 파일)
prompt-compiler input.prompt --format=single
```

## 프롬프트 파일 작성

`prompts` 디렉토리에 `.prompt` 파일을 작성합니다:

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

## 프로그래밍 방식 사용

```python
from pathlib import Path
from prompt_compiler.compiler import Compiler
from prompt_compiler.ai_adapters import GptAdapter

# AI 어댑터 초기화
adapter = GptAdapter(api_key="your-api-key")

# 컴파일러 초기화
compiler = Compiler(adapter)

# 프롬프트로부터 코드 생성
result = compiler.compile(Path("prompts/example.prompt"))

# 생성된 코드와 테스트 출력
print("Generated Code:")
print(result["code"])
print("\nGenerated Tests:")
print(result["tests"])
```

## 고급 기능

### 캐싱 사용

```python
compiler = Compiler(adapter, cache_dir=Path(".cache"))
result = compiler.compile(prompt_file, force_rebuild=False)  # 캐시 사용
```

### 커스텀 포맷터 사용

```python
from prompt_compiler.formatters import CodeFormatter, ResponseProcessor

class CustomFormatter(CodeFormatter):
    def format(self, code: str) -> str:
        # 커스텀 포맷팅 로직
        return code

formatter = ResponseProcessor(CustomFormatter())
compiler = Compiler(adapter, formatter=formatter)
```

### 커스텀 템플릿 사용

```python
from prompt_compiler.templates import BaseTemplate

class CustomTemplate(BaseTemplate):
    def get_system_prompt(self) -> str:
        return "Custom system prompt..."

    def get_template(self) -> str:
        return "Custom template string..."

compiler = Compiler(adapter, template=CustomTemplate())
```

## 에러 처리

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

## 개발

- 테스트 실행: `poetry run pytest`
- 코드 포맷팅: `poetry run black .`
- 임포트 정렬: `poetry run isort .`
- 타입 체크: `poetry run mypy .`

## 라이선스

MIT License

