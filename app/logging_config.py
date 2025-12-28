import logging
import logging.config
import os


def configure_logging(level: str | None = None) -> None:
    """Configure application-wide logging.

    Args:
        level: Optional log level (e.g. "DEBUG", "INFO"). If None, reads
            from LOG_LEVEL env var or defaults to "INFO".
    """
    level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            }
        },
        "root": {"handlers": ["console"], "level": level},
        "loggers": {
            # Example project-level logger; modules should use getLogger(__name__)
            "ai_qa_assignment": {"handlers": ["console"], "level": level, "propagate": False}
        },
    }

    logging.config.dictConfig(LOGGING)
    logging.getLogger(__name__).info("Logging configured, level=%s", level)
