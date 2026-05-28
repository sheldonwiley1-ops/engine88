# wsgi.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hardware_bridge import app as application
