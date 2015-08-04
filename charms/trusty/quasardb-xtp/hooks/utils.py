#!/usr/bin/env python
import json

QDBD_CONFIG_FILE = "/etc/qdb/qdbd.conf"
QDB_HTTPD_CONFIG_FILE   = "/etc/qdb/qdb_httpd.conf"

def load_config_file(f):
    with open(f, 'rb') as f:
        return json.load(f)

def save_config_file(f, d):
    with open(f, 'wb') as f:
        json.dump(d, f)

def make_hostname(hostname, port):
    return hostname + ':' + str(port)

class BaseConfig(object):

    def __load(self):
        self.__config = load_config_file(self.__location)

    def save(self):
        save_config_file(self.__location, self.__config)

    def __init__(self, location):
        self.__location = location
        self.__load()

    def config(self):
        return self.__config

class QdbConfig(BaseConfig):

    def __init__(self, location = QDBD_CONFIG_FILE):
        super(QdbConfig, self).__init__(location)

    def set_hostname(self, hostname, qdb_port):
        self.config()['local']['network']['listen_on'] = make_hostname(hostname, qdb_port)

    def set_timeout(self, client_timeout, idle_timeout):
        self.config()['local']['network']['client_timeout'] = int(client_timeout)
        self.config()['local']['network']['idle_timeout'] = int(idle_timeout)

    def set_limiter(self, max_bytes, max_count):
        self.config()['global']['limiter']['max_bytes'] = int(max_bytes)
        self.config()['global']['limiter']['max_in_entries_count'] = int(max_count)

    def set_peer(self, remote_hostname, remote_qdb_port):
        self.config()['local']['chord']['bootstrapping_peers'] = [ make_hostname(remote_hostname, remote_qdb_port) ]

class QdbHttpdConfig(BaseConfig):

    def __init__(self, location = QDB_HTTPD_CONFIG_FILE):
        super(QdbHttpdConfig, self).__init__(location)

    def set_hostname(self, hostname, admin_port, qdb_port):
        self.config()['listen_on'] = make_hostname(hostname, admin_port)
        self.config()['remote_node'] = make_hostname(hostname, qdb_port)

def set_hostname(hostname, qdb_port, admin_port):
    qdb_config = QdbConfig()
    qdb_config.set_hostname(hostname, qdb_port)
    qdb_config.save()

    qdb_httpd_config = QdbHttpdConfig()
    qdb_httpd_config.set_hostname(hostname, admin_port, qdb_port)
    qdb_httpd_config.save()

def set_timeout(client_timeout, idle_timeout):
    qdb_config = QdbConfig()
    qdb_config.set_timeout(client_timeout, idle_timeout)
    qdb_config.save()

def set_limiter(max_bytes, max_count):
    qdb_config = QdbConfig()
    qdb_config.set_limiter(max_bytes, max_count)
    qdb_config.save()  

def set_peer(remote_hostname, remote_qdb_port):
    qdb_config = QdbConfig()
    qdb_config.set_peer(remote_hostname, remote_qdb_port)
    qdb_config.save()