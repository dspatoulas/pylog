# PyLog: A colorful python logging formatter

The colorful `pylog` logging format was inspired by the `tracing` library in Rust 🦀.

## Basic Usage

The `PrettyTextFormatter` can be used as the `logger_formatter` when instantiating 
a new instance of the `Logger` from the `aws_lambda_powertools` library.

```python
from aws_lambda_powertools.logging import Logger
from pylog.formatter import PrettyTextFormatter

logger = Logger(
    "example-service",
    logger_formatter=PrettyTextFormatter(),
)

logger.info("Test log message with attrs", my_custom_attr="some-value")
```

## Advanced Usage

Checkout the `example.py` for a more complex example of how to dynamically configure the 
`logger_formatter` in python applications, scripts or modules.
