"""pytest setup: make `api/` importable the same way the Vercel functions do."""
import os
import sys

API_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api")
if API_DIR not in sys.path:
    sys.path.insert(0, API_DIR)
