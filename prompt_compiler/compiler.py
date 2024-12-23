from pathlib import Path
from typing import Dict, Any

from prompt_compiler.prompt_reader import PromptReader
from prompt_compiler.code_generator import CodeGenerator
from prompt_compiler.test_generator import TestGenerator
from prompt_compiler.validator import Validator


class Compiler:
    def __init__(self):
        self.prompt_reader = PromptReader()
        self.code_generator = CodeGenerator()
        self.test_generator = TestGenerator()
        self.validator = Validator()

    def compile(self, prompt_file: Path) -> Dict[str, Any]:
        """
        Compile a prompt file into code and tests.

        Args:
            prompt_file: Path to the prompt file

        Returns:
            Dictionary containing generated code and tests
        """
        # Read and parse prompt file
        prompt_data = self.prompt_reader.read(prompt_file)

        # Generate code from prompt
        generated_code = self.code_generator.generate(prompt_data)

        # Generate tests
        generated_tests = self.test_generator.generate(generated_code)

        # Validate generated code
        self.validator.validate(generated_code)

        return {"code": generated_code, "tests": generated_tests}
