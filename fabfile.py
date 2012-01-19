from fabric.api import *
from fabric.contrib.project import rsync_project
import os
env.hosts = ["ubuntu@feedify.movieos.org"]

DEPLOY = "~/feedify"

def shell(*cmd):
    import subprocess
    run = ["ssh", "-A", "-t", env.host_string]
    run += cmd
    print ' '.join(run)
    subprocess.call(run)

def bootstrap():
    packages = [
        "python", "python-virtualenv", "gunicorn", "python-mysqldb",
        "mysql-server", "memcached", "mysql-client",
        "nginx", "joe", "munin", "munin-node",
    ]
    sudo("apt-get update")
    sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y %s"%(" ".join(packages)), shell=True)

    run("if [ ! -d ~/venv ]; then virtualenv ~/venv; fi")

    put("deploy/gunicorn.conf", "/etc/gunicorn.d/feedify.py", use_sudo=True)
    put("deploy/nginx.conf", "/etc/nginx/sites-enabled/feedify.conf", use_sudo=True)
    sudo("/etc/init.d/gunicorn restart")
    sudo("/etc/init.d/nginx restart")

    run("(echo 'create database feedify charset=utf8' | mysql -uroot) || true")

    # DB setup is your problem now.





def deploy():
    run("mkdir -p %s"%DEPLOY)
    rsync_project(
        local_dir="./",
        remote_dir="%s/"%DEPLOY,
        exclude=["venv", "*.pyc"],
        #delete=True,
    )

    run("~/venv/bin/pip install -q -r %s/requirements.txt"%DEPLOY)
    
    run("cd %s && ~/venv/bin/python manage.py migrate"%DEPLOY)
    sudo("/etc/init.d/gunicorn reload")
    


def get_database():
    run("mysqldump -uroot zebra | gzip -c > /tmp/zebra-dump.sql.gz", shell=False)
    get("/tmp/zebra-dump.sql.gz", "/tmp/zebra-dump.sql.gz")
    os.system("gzip -cd /tmp/zebra-dump.sql.gz | mysql -uroot zebra")

