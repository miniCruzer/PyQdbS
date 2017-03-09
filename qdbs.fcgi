#!/usr/bin/python3.5

from flup.server.fcgi import WSGIServer
from PyQdbS import create_app

if __name__ == '__main__':
    WSGIServer(create_app("ProductionConfig"), bindAddress='/var/lib/qdbs/fcgi.sock').run()