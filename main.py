"""Compatibility entry point for the Streamlit dashboard.

Run with: streamlit run main.py
"""

# Importing the module builds and runs the dashboard.  Keeping this wrapper
# lets existing `streamlit run main.py` commands continue to work.
import src.main  # noqa: F401,E402
