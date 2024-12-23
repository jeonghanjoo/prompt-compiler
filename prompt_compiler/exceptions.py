from typing import Optional


class PromptCompilerError(Exception):
    """Base exception for all prompt compiler errors."""

    pass


class AIAdapterError(PromptCompilerError):
    """Base exception for AI adapter related errors."""

    def __init__(self, message: str, model: str, raw_error: Optional[Exception] = None):
        self.model = model
        self.raw_error = raw_error
        super().__init__(f"{model} error: {message}")


class RateLimitError(AIAdapterError):
    """Raised when AI API rate limit is exceeded."""

    def __init__(self, model: str, retry_after: Optional[int] = None):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after} seconds.", model
        )


class ValidationError(PromptCompilerError):
    """Raised when generated code validation fails."""

    pass


class CacheError(PromptCompilerError):
    """Raised when cache operations fail."""

    pass
