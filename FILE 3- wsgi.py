# wsgi.py - WSGI configuration for PythonAnywhere
# Points to hardware_bridge:application

import sys
import os

# Add project directory to path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Import the application from hardware_bridge
try:
    from hardware_bridge import app as application
except ImportError:
    # Fallback to coherence_engine if hardware_bridge not available
    from coherence_engine import app as application

# Set environment variables
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('ENGINE_MODE', 'deterministic')

# Ensure deterministic integrity
application.config['DETERMINISTIC_MODE'] = True
application.config['HARMONIC_CONSTRAINT'] = 1.618033988749895