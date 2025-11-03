#!/usr/bin/env python3
"""
SigmaRecon - 2026-Ready Attack Surface Discovery Tool

A comprehensive reconnaissance platform that unifies 23+ subdomain enumeration tools,
provides a resilient data collection pipeline, and supports extensible configuration management.
"""

__version__ = "1.0.2"
__author__ = "El3aref"
__description__ = "The Ultimate Subdomain Enumeration Tool for 2026"

# Import main CLI class and function for easy access
from .main import SigmaReconCLI, main

# Define what gets imported with "from sigmarecon import *"
__all__ = [
    'SigmaReconCLI',
    'main',
    '__version__',
    '__author__', 
    '__description__'
]