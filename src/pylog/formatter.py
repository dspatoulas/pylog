from typing import Any

from aws_lambda_powertools.logging.formatter import LambdaPowertoolsFormatter
from aws_lambda_powertools.logging.types import LogRecord


# ANSI escape codes for styling
RESET = "\033[0m"
ITALIC = "\033[3m"
ATTRS = "\033[90m"
COLORS = {
    "DEBUG": "\033[94m",  # Blue
    "INFO": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[95m",  # Magenta
}
STANDARD_LOG_ATTRS = [
    "timestamp",
    "level",
    "location",
    "message",
    "exception",
    "stack_trace",
]


class PrettyTextFormatter(LambdaPowertoolsFormatter):
    _enable_ascii_colors: bool

    def __init__(
        self,
        enable_ascii_colors: bool = True,
        location: str = "%(module)s:%(funcName)s:%(lineno)d",
        *args,
        **kwargs,
    ):
        super().__init__(location=location, *args, **kwargs)
        self._enable_ascii_colors = enable_ascii_colors

    def format_key_value_pair(self, key: str, value: Any) -> str:
        formatted_kv_pair = (
            f"{ATTRS}{key}={RESET}{ITALIC}{self.json_serializer(value)}{RESET}"
            if self._enable_ascii_colors
            else f"{key}={value}"
        )
        return formatted_kv_pair

    def serialize(self, log: LogRecord):
        # Set the default log attributes
        log_context = f"{log['timestamp']} {log['level']} {log['location']}"
        log_message = log["message"]

        exception = log.get("exception")
        if exception:
            log_message = f"{log_message}\n{exception}"

        formatted_kv_pairs = []
        for key, value in log.items():
            if key in STANDARD_LOG_ATTRS:
                # Skip the standard attrs to avoid duplicates serialization
                continue

            formatted_kv_pair = self.format_key_value_pair(key, value)
            formatted_kv_pairs.append(formatted_kv_pair)

        # Build the formatted set of key-value pairs
        formatted_log_attrs = ", ".join(formatted_kv_pairs)

        # Used to set the ascii color of log record (if enabled)
        log_level = log["level"].upper()

        # Final serialization of the log record with optional ascii colors
        formatted_log = (
            f"{COLORS[log_level]}{log_context}{RESET} {log_message} {formatted_log_attrs}"
            if self._enable_ascii_colors is True
            else f"{log_context} {log_message} {formatted_log_attrs}"
        )

        return formatted_log
