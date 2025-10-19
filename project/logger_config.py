import os
import colorlog


def get_logging_config(BASE_DIR):
    """
    Returns the logging configuration dictionary.
    Requires BASE_DIR to correctly set up the log file path.
    """
    LOG_DIR = os.path.join(BASE_DIR, "media", "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "color": {
                "()": "colorlog.ColoredFormatter",
                "format": (
                    "%(log_color)s[{levelname:<8}] {asctime} | "
                    "{name} (%(filename)s:%(lineno)d) — %(message)s"
                ),
                "style": "%",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
            "verbose": {
                "format": "[{levelname}] {asctime} {name} {module} — {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "color",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "verbose",
                "filename": os.path.join(LOG_DIR, "project.log"),
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": True,
            },
            "dummyapp": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "celerydummyapp": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "pdfsummarizer": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
    return LOGGING
