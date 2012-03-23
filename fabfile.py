from fabric.api import *
from fabric.contrib.project import rsync_project
import os
env.hosts = ["ubuntu@feedify.movieos.org"]

DEPLOY = "~/feedify"
VENV = "/home/ubuntu/venv_feedify"

def shell(*cmd):
    import subprocess
    run = ["ssh", "-A", "-t", env.host_string]
    run += cmd
    print ' '.join(run)
    subprocess.call(run)

def sync_files():
    run("mkdir -p %s"%DEPLOY)
    rsync_project(
        local_dir="./",
        remote_dir="%s/"%DEPLOY,
        exclude=["venv", "*.pyc"],
        #delete=True,
    )

def bootstrap():
    sync_files()

    packages = [
        "python", "python-virtualenv", "python-mysqldb",
        "mysql-server", "memcached", "mysql-client",
        "nginx", "joe", "munin", "munin-node",
    ]
    sudo("apt-get update")
    sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y %s"%(" ".join(packages)), shell=True)

    run("if [ ! -d %s ]; then virtualenv %s; fi"%(VENV, VENV))

    sudo("mkdir -p /var/log/feedify")
    sudo("chown ubuntu:ubuntu /var/log/feedify /var/log/feedify/*")

    sudo("ln -sf %s/deploy/nginx.conf /etc/nginx/sites-enabled/feedify.conf"%DEPLOY)

    # can't be symlink, alas. upstart gets stroppy.
    sudo("cp -f %s/deploy/gunicorn.conf /etc/init/feedify.conf"%DEPLOY)

    sudo("/etc/init.d/nginx configtest && /etc/init.d/nginx reload")

    run("(echo 'create database feedify charset=utf8' | mysql -uroot) || true")

    # DB setup is your problem now.


def deploy():
    sync_files()
    run("%s/bin/pip install -q -r %s/requirements.txt"%(VENV, DEPLOY))
    run("cd %s && %s/bin/python manage.py migrate"%(DEPLOY, VENV))
    sudo("reload feedify")

def get_database():
    run("mysqldump -uroot feedify | gzip -c > /tmp/feedify-dump.sql.gz", shell=False)
    get("/tmp/feedify-dump.sql.gz", "/tmp/feedify-dump.sql.gz")
    os.system("gzip -cd /tmp/feedify-dump.sql.gz | mysql -uroot feedify")

