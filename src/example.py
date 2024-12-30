from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.logging.formatters.datadog import DatadogLogFormatter

from pylog.formatter import PrettyTextFormatter
from pylog.settings import LogLevel, LogFormat, LoggerSettings


def get_logger(service_name: str, cfg: LoggerSettings) -> Logger:
    """
    A standard way for python modules to initialize the standard logger and
    comes with a reasonable set of default configuration values.
    :param cfg:
    :param service_name:
    :return:
    """
    enable_ascii_colors = cfg.log_format == LogFormat.TextPretty
    logger_formatter = (
        DatadogLogFormatter()
        if cfg.log_format == LogFormat.JSON
        else PrettyTextFormatter(
            enable_ascii_colors=enable_ascii_colors,
        )
    )
    return Logger(
        service=service_name,
        logger_formatter=logger_formatter,
        level=cfg.log_level,
    )


def some_function_that_raises(logger: Logger):
    try:
        is_ok = False
        logger.append_keys(is_ok=is_ok)

        logger.info(
            "Important conditions in the application should be logged with context",
            should_panic="NOT_YET",
        )

        logger.debug(
            "Debug logs can be more verbose and shouldn't be left on in production",
            should_panic="SOON",
        )
        # Simulating an error
        result = 1 / 0

        logger.critical(
            "How did we get this far? 😉",
            is_ok=False,
            should_panic="YES",
            result=result,
        )

    except ZeroDivisionError as e:
        # Log an error with the exception passed directly
        logger.error(
            "Something bad happened 😅",
            exc_info=e,
            should_panic="TOO_LATE",
            is_ok=False,
        )


def main():
    """
    There are fancier things to wire up, but for now this will instantiate
    a structured logging format that can be toggled between different
    output formats depending on the environment variables at run-time
    """
    default_config = LoggerSettings()

    # Defaults to `PrettyText` format
    pretty_text_logger = get_logger("example-pretty-text", default_config)

    # Checkout the default logger in action
    some_function_that_raises(pretty_text_logger)

    # Change to `JSON` (DataDog) format
    datadog_logger = get_logger(
        "example-json",
        LoggerSettings(
            log_level=LogLevel.Debug,
            log_format=LogFormat.JSON,
        ),
    )

    # Compare the output format of the log records
    some_function_that_raises(datadog_logger)


if __name__ == "__main__":
    main()
