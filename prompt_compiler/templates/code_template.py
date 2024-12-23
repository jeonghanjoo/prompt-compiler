from .base_template import BaseTemplate


class CodeGenerationTemplate(BaseTemplate):
    """Template for code generation prompts."""

    def get_system_prompt(self) -> str:
        return """You are an expert programmer. Your task is to generate high-quality, 
        well-documented code based on the given specifications. Follow these guidelines:
        
        1. Write clean, maintainable code
        2. Include appropriate documentation
        3. Follow the specified template structure
        4. Use proper error handling
        5. Follow language-specific best practices
        """

    def get_template(self) -> str:
        return """
        Generate code based on the following specifications:
        
        Name: {{ name }}
        Description: {{ description }}
        {% if template %}
        Template Structure:
        ```
        {{ template }}
        ```
        {% endif %}
        
        Additional Requirements:
        {% if requirements %}
        {% for req in requirements %}
        - {{ req }}
        {% endfor %}
        {% endif %}
        
        Language: {{ language|default('python') }}
        
        Please provide the implementation with appropriate documentation and error handling.
        """
