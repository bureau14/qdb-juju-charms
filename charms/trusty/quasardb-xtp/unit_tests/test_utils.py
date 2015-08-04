#!/usr/bin/env python

import sys
import unittest
from pkg_resources import resource_filename

# allow importing actions from the hooks directory
sys.path.append(resource_filename(__name__, '../hooks'))

import utils


class TestUtils(unittest.TestCase):
    
    def test_qdb_config_test(self):
        c = utils.QdbConfig("./data/qdbd.conf")

        c.set_hostname("fake", 1337)
        c.set_timeout(1, 2)
        c.set_limiter(3, 4)
        c.set_peer("other", 666)

        cfg = c.config()

        self.assertEqual(cfg['local']['network']['listen_on'], "fake:1337")
        self.assertEqual(cfg['local']['network']['client_timeout'], 1)
        self.assertEqual(cfg['local']['network']['idle_timeout'], 2)
        self.assertEqual(len(cfg['local']['chord']['bootstrapping_peers']), 1)
        self.assertEqual(cfg['local']['chord']['bootstrapping_peers'][0], "other:666")

        self.assertEqual(cfg['global']['limiter']['max_bytes'], 3)
        self.assertEqual(cfg['global']['limiter']['max_in_entries_count'], 4)

        c.save()

        # reload have our changes

        c2 = utils.QdbConfig("./data/qdbd.conf")

        self.assertEqual(cfg['local']['network']['listen_on'], "fake:1337")
        self.assertEqual(cfg['local']['network']['client_timeout'], 1)
        self.assertEqual(cfg['local']['network']['idle_timeout'], 2)
        self.assertEqual(len(cfg['local']['chord']['bootstrapping_peers']), 1)
        self.assertEqual(cfg['local']['chord']['bootstrapping_peers'][0], "other:666")

        self.assertEqual(cfg['global']['limiter']['max_bytes'], 3)

    def test_qdb_httpd_config_test(self):

        c = utils.QdbHttpdConfig("./data/qdb_httpd.conf")

        c.set_hostname("fake", 1337, 8888)

        cfg = c.config()

        self.assertEqual(cfg['listen_on'], "fake:1337")
        self.assertEqual(cfg['remote_node'], "fake:8888")

        c.save()

        c2 = utils.QdbHttpdConfig("./data/qdb_httpd.conf")

        self.assertEqual(cfg['listen_on'], "fake:1337")
        self.assertEqual(cfg['remote_node'], "fake:8888")

if __name__ == '__main__':
    unittest.main()
