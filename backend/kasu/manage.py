#!/usr/bin/env python
"""Script de gestion Django pour KASU."""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Django n'est pas installé. Lancez: pip install -r requirements.txt"
        )
    execute_from_command_line(sys.argv)
