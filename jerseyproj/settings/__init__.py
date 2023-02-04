from .base import *
if os.environ['devmode'] == 'prod':
   from .prod import *
else:
   from .dev import *