"""Pytest configuration to ensure proper root path resolution."""

import os
import sys

# Prepend project root to sys.path so 'src' and 'security' packages import cleanly
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
