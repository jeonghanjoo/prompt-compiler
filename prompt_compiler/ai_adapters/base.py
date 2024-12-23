from abc import ABC, abstractmethod


class AiAdapter(ABC):
    """Base class for AI model adapters."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate code using the AI model.

        Args:
            prompt: The prompt to send to the AI model
            **kwargs: Additional model-specific parameters

        Returns:
            Generated code as string
        """
        pass

    @abstractmethod
    def validate_response(self, response: str) -> bool:
        """
        Validate the AI model's response.

        Args:
            response: The response from the AI model

        Returns:
            True if response is valid, False otherwise
        """
        pass
