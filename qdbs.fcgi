#!/usr/bin/python3.5

from flup.server.fcgi import WSGIServer
from main import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/var/lib/qdbs/fcgi.sock').run()