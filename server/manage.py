#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.error(
            "WTF is this cant import django BS", exc_info=exc)
        raise ImportError(
            "same message again, it was working just now!"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
