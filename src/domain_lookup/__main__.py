#!/usr/bin/env python3
"""
Entry point for the domain_lookup package.
This allows the package to be run as a module using python -m domain_lookup
"""

from .cli import main

if __name__ == "__main__":
    main()
