import sys
sys.path.insert(0, '/home/user/workspace/frodo')
from web import app as application
sys.stdout = sys.stderr
import logging
logging.basicConfig(stream=sys.stderr)
