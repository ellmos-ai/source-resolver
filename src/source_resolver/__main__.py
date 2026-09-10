"""Executable module entry point for python -m source_resolver."""

from __future__ import annotations

import sys

from source_resolver.cli import main

if __name__ == "__main__":
    sys.exit(main())
