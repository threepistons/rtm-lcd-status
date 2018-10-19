#!/usr/bin/python

from py_daemon import py_daemon
# import py_daemon

class RTMTicker(py_daemon.Daemon):
    def run(self):
        print('Hello Lucky')
        
ticker = RTMTicker('~/test.pid')
ticker.start()
