#!/usr/bin/env python

from charmhelpers.core import hookenv

def log_start(service_name):
    hookenv.log('quasardb ' + service_name + ' starting')
