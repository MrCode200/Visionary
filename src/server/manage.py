#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys

from magic_utils.custom_logger import setup_logger


def main():
    if not os.path.exists("logs"):
        os.mkdir("logs")

    setup_logger(
        logger_name="hijacker.app",
        stream_level=logging.DEBUG,
        log_file_name="logs/hijacker.log",
        stream_in_color = True,
        log_in_json = True,
        extra_log_args=None,
    )

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
