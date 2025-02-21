"""Environment configuration and utilities."""

import os
from contextlib import contextmanager
from functools import wraps
from typing import Generator, List, Optional, Union


class Environment:
    """Environment configuration and utilities."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    def __init__(self) -> None:
        self._env = os.getenv("PYTHON_ENV", self.DEVELOPMENT)

    @property
    def current(self) -> str:
        """Get current environment name."""
        return self._env

    def is_development(self) -> bool:
        """Check if current environment is development."""
        return self._env == self.DEVELOPMENT

    def is_production(self) -> bool:
        """Check if current environment is production."""
        return self._env == self.PRODUCTION

    def is_testing(self) -> bool:
        """Check if current environment is testing."""
        return self._env == self.TESTING

    def in_environment(self, *environments: str) -> bool:
        """Check if current environment is in given environments."""
        return self._env in environments

    @contextmanager
    def include(self, environments: Union[str, List[str]]) -> Generator[Optional[None], None, None]:
        """Context manager for environment-specific code blocks."""
        envs = [environments] if isinstance(environments, str) else environments
        if self._env in envs:
            yield
        else:
            yield None

    @contextmanager
    def exclude(self, environments: Union[str, List[str]]):
        """Context manager for excluding specific environments."""
        envs = [environments] if isinstance(environments, str) else environments
        if self._env not in envs:
            yield
        else:
            yield None

    def requires_env(
        self,
        include: Optional[Union[str, List[str]]] = None,
        exclude: Optional[Union[str, List[str]]] = None,
    ):
        """Decorator for environment-specific functions."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if include:
                    includes = [include] if isinstance(include, str) else include
                    if self._env not in includes:
                        return None

                if exclude:
                    excludes = [exclude] if isinstance(exclude, str) else exclude
                    if self._env in excludes:
                        return None

                return func(*args, **kwargs)

            return wrapper

        return decorator


# Create global instance
environment = Environment()
