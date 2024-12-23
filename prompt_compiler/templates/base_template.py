from abc import ABC, abstractmethod
from typing import Dict, Any
from jinja2 import Environment, BaseLoader


class BaseTemplate(ABC):
    """Base class for prompt templates."""

    def __init__(self):
        self.env = Environment(loader=BaseLoader())

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI model."""
        pass

    @abstractmethod
    def get_template(self) -> str:
        """Get the template string."""
        pass

    def render(self, context: Dict[str, Any]) -> str:
        """Render the template with given context."""
        template = self.env.from_string(self.get_template())
        return template.render(**context)
