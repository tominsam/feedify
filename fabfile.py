import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deployinator"))
from deployinator.deployinator import *

fab_init("feedify",
    database = "feedify",
    rules = {
        "nginx": "deploy/nginx.conf",
        "gunicorn": {
            "port": 8002,
        }
    }
)
