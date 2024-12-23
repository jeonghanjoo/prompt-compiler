from anthropic import Anthropic
from .base import AiAdapter


class ClaudeAdapter(AiAdapter):
    """Adapter for Anthropic's Claude models."""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        """
        Initialize Claude adapter.

        Args:
            api_key: Anthropic API key
            model: Claude model to use (default: claude-3-opus-20240229)
        """
        self.api_key = api_key
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate code using Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")

    def validate_response(self, response: str) -> bool:
        """Validate Claude response."""
        # Basic validation - check if response is not empty
        return bool(response and response.strip())
