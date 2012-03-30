import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))
from fabutils import *

fab_init("feedify",
    rules = {
        "nginx": "deploy/nginx.conf",
        "database": "feedify",
        "gunicorn": {
            "port": 8002,
        }
    }
)
