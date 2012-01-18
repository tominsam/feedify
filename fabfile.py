from fabric.api import *
import os
import urllib

def deploy():
    os.system("epio upload")
    os.system("epio django migrate")
    urllib.urlopen("http://feedify.movieos.org").read() # kick unicorn
