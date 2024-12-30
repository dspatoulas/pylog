from enum import Enum

from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    Debug = "DEBUG"
    Info = "INFO"
    Warning = "WARNING"
    Error = "ERROR"
    Critical = "CRITICAL"


class LogFormat(str, Enum):
    JSON = "JSON"
    TextPretty = "TextPretty"
    Text = "Text"


class LoggerSettings(BaseSettings):
    log_level: LogLevel = LogLevel.Info
    log_format: LogFormat = LogFormat.TextPretty

    def enable_ascii_colors(self) -> bool:
        return self.log_format == LogFormat.TextPretty
