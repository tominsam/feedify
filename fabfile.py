from fabric.api import *
from fabric.contrib.project import rsync_project
import os
env.hosts = ["tomi@seatbelt.jerakeen.org"]

DEPLOY = "~/deploy/feedify"

def deploy():
    run("mkdir -p %s"%DEPLOY)
    rsync_project(
        local_dir="./",
        remote_dir="%s/"%DEPLOY,
        exclude=["venv", "*.pyc"],
        #delete=True,
    )

    run("/home/tomi/deploy/venv/bin/pip install -q -r %s/requirements.txt"%DEPLOY)
    
    run("cd %s && ../venv/bin/python manage.py migrate"%DEPLOY)
    sudo("/etc/init.d/gunicorn_feedify reload")
    


def get_database():
    run("mysqldump -uroot feedify | gzip -c > /tmp/feedify-dump.sql.gz", shell=False)
    get("/tmp/feedify-dump.sql.gz", "/tmp/feedify-dump.sql.gz")
    os.system("echo \"drop database feedify; create database feedify charset=utf8;\" | mysql -uroot")
    os.system("gzip -cd /tmp/feedify-dump.sql.gz | mysql -uroot feedify")

