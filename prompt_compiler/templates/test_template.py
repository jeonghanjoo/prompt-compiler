from .base_template import BaseTemplate


class TestGenerationTemplate(BaseTemplate):
    """Template for test generation prompts."""

    def get_system_prompt(self) -> str:
        return """You are an expert in test-driven development. Your task is to generate 
        comprehensive test cases for the given code. Follow these guidelines:
        
        1. Cover edge cases
        2. Include both positive and negative test cases
        3. Use appropriate test frameworks
        4. Write clear test descriptions
        5. Follow testing best practices
        """

    def get_template(self) -> str:
        return """
        Generate test cases for the following code:

        ```{{ language|default('python') }}
        {{ code }}
        ```
        
        Test Requirements:
        {% if requirements %}
        {% for req in requirements %}
        - {{ req }}
        {% endfor %}
        {% endif %}
        
        Framework: {{ framework|default('pytest') }}
        
        Please provide comprehensive test cases with appropriate assertions and error cases.
        """
