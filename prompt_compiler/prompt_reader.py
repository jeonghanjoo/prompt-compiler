from pathlib import Path
from typing import Dict, Any
import yaml


class PromptReader:
    def read(self, prompt_file: Path) -> Dict[str, Any]:
        """
        Read and parse a prompt file.

        Args:
            prompt_file: Path to the prompt file

        Returns:
            Dictionary containing parsed prompt data
        """
        with open(prompt_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse YAML format
        try:
            prompt_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse prompt file: {e}")

        return prompt_data
