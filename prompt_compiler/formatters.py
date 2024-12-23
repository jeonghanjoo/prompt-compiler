import re
from typing import Dict, Any
from abc import ABC, abstractmethod
from .exceptions import ValidationError


class CodeFormatter(ABC):
    """Base class for code formatters."""

    @abstractmethod
    def format(self, code: str) -> str:
        """Format the code string."""
        pass


class PythonFormatter(CodeFormatter):
    """Formatter for Python code."""

    def format(self, code: str) -> str:
        """Format Python code."""
        # Extract code blocks if present
        code = self._extract_code_blocks(code)

        # Remove extra blank lines
        code = re.sub(r"\n\s*\n\s*\n", "\n\n", code)

        # Ensure proper indentation
        lines = code.split("\n")
        formatted_lines = []
        indent_level = 0

        for line in lines:
            # Adjust indent level based on line content
            stripped = line.strip()
            if stripped.endswith(":"):
                formatted_lines.append("    " * indent_level + stripped)
                indent_level += 1
            elif stripped in ["pass", "break", "continue"]:
                formatted_lines.append("    " * indent_level + stripped)
            elif stripped:
                formatted_lines.append("    " * indent_level + stripped)
            else:
                formatted_lines.append("")

        return "\n".join(formatted_lines)

    def _extract_code_blocks(self, text: str) -> str:
        """Extract code from markdown-style code blocks."""
        code_block_pattern = r"```(?:python)?\n(.*?)\n```"
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        return matches[0] if matches else text


class ResponseProcessor:
    """Process and validate AI responses."""

    def __init__(self, formatter: CodeFormatter):
        self.formatter = formatter

    def process(self, response: str, context: Dict[str, Any]) -> str:
        """
        Process and validate the AI response.

        Args:
            response: Raw response from AI
            context: Original context used to generate the response

        Returns:
            Processed and formatted code
        """
        # Format the code
        formatted_code = self.formatter.format(response)

        # Validate the formatted code
        self._validate_code(formatted_code, context)

        return formatted_code

    def _validate_code(self, code: str, context: Dict[str, Any]) -> None:
        """
        Validate the processed code.

        Args:
            code: Processed code
            context: Original context

        Raises:
            ValidationError: If code doesn't meet requirements
        """
        required_elements = context.get("required_elements", [])
        for element in required_elements:
            if element not in code:
                raise ValidationError(f"Missing required element: {element}")
