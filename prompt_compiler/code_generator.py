from pathlib import Path
from typing import Dict, Any, Optional
from .ai_adapters import AiAdapter
from .utils.cache_manager import CacheManager
from .exceptions import ValidationError
from .templates import CodeGenerationTemplate
from .formatters import ResponseProcessor, PythonFormatter


class CodeGenerator:
    def __init__(
        self,
        ai_adapter: AiAdapter,
        cache_dir: Optional[Path] = None,
        template: Optional[CodeGenerationTemplate] = None,
        formatter: Optional[ResponseProcessor] = None,
    ):
        """
        Initialize CodeGenerator with an AI adapter.

        Args:
            ai_adapter: AI adapter instance to use for code generation
            cache_dir: Directory for caching responses (optional)
            template: Template for code generation (optional)
            formatter: Response formatter (optional)
        """
        self.ai_adapter = ai_adapter
        self.cache_manager = CacheManager(cache_dir or Path(".cache"))
        self.template = template or CodeGenerationTemplate()
        self.formatter = formatter or ResponseProcessor(PythonFormatter())

    def generate(self, prompt_data: Dict[str, Any], force_rebuild: bool = False) -> str:
        """
        Generate code from prompt data using the configured AI adapter.

        Args:
            prompt_data: Dictionary containing parsed prompt data
            force_rebuild: If True, ignore cache and generate new code

        Returns:
            Generated code as string
        """
        if not force_rebuild:
            cached_response = self.cache_manager.get_cached_response(prompt_data)
            if cached_response:
                return cached_response

        # Format prompt using template
        formatted_prompt = self.template.render(prompt_data)
        system_prompt = self.template.get_system_prompt()

        # Generate code using AI adapter
        generated_code = self.ai_adapter.generate(
            formatted_prompt, system_prompt=system_prompt
        )

        # Process and format the response
        processed_code = self.formatter.process(generated_code, prompt_data)

        # Validate generated code
        if not self.ai_adapter.validate_response(processed_code):
            raise ValidationError("Generated code validation failed")

        # Cache the response
        self.cache_manager.cache_response(prompt_data, processed_code)

        return processed_code
