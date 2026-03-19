from logging import getLevelNamesMapping
from typing import Literal

from pydantic import BaseModel


class LoggerConfig(BaseModel):
    format: str = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    @property
    def log_level(self) -> int:
        return getLevelNamesMapping()[self.level]