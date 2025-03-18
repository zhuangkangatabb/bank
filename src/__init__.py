# This file marks the src/ directory as a Python package.
# Optionally, you can expose key components for easier imports.

from .banking_api import app  # Expose the FastAPI app for running the API

__all__ = ["app"]  # Define what gets imported with `from src import *`
