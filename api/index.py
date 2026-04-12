import os
import sys

# Add the parent directory to sys.path so we can import from the 'fastapi' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.main import app
