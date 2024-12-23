import openai
from typing import Dict, Any, Optional
from openai import OpenAIError
from .base import AiAdapter
from ..exceptions import AIAdapterError, RateLimitError
from ..utils.rate_limiter import RateLimiter


class GptAdapter(AiAdapter):
    """Adapter for OpenAI's GPT models."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize GPT adapter.

        Args:
            api_key: OpenAI API key
            model: GPT model to use (default: gpt-4)
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    @RateLimiter(calls=50, period=60)  # 50 calls per minute
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate code using GPT."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful programming assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            if "rate limit" in str(e).lower():
                raise RateLimitError(model=self.model)
            raise AIAdapterError(str(e), self.model, e)
        except Exception as e:
            raise AIAdapterError(f"Unexpected error: {str(e)}", self.model, e)

    def validate_response(self, response: str) -> bool:
        """Validate GPT response."""
        # Basic validation - check if response is not empty
        return bool(response and response.strip())
