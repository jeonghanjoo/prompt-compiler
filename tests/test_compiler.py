from pathlib import Path
import pytest
from prompt_compiler.compiler import Compiler


def test_compiler_initialization():
    compiler = Compiler()
    assert compiler is not None


def test_compile_example_prompt(tmp_path):
    # Create a temporary prompt file
    prompt_content = """
    name: Test
    description: Test prompt
    template: |
      def hello():
          return "Hello"
    """
    prompt_file = tmp_path / "test.prompt"
    prompt_file.write_text(prompt_content)

    # Compile the prompt
    compiler = Compiler()
    result = compiler.compile(prompt_file)

    assert "code" in result
    assert "tests" in result
