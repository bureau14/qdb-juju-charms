# change this if needed
VERSION = "2.0/beta4"

# you may want to change this

SERVER_DEB          = "server/qdb-server_2.0.0-1.deb"
SERVER_DEB_SHA1   = "3c2b700629a26b20b8d29eb220fc25af6cb403e8"

UTILS_DEB           = "utils/qdb-utils_2.0.0-1.deb"
UTILS_DEB_SHA1    = "b0c15732a03aa6c4221f5195c0cebd0883e8e30c"

CAPI_DEB            = "api/c/qdb-api_2.0.0-1.deb"
CAPI_DEB_SHA1     = "2a9b6bcd4660a04f20eccaf1ee8119c9fa0bf862"

# don't change this
__base_dl_url = "https://download.quasardb.net/quasardb/"

__debs = { 
    SERVER_DEB: SERVER_DEB_SHA1,
    UTILS_DEB: UTILS_DEB_SHA1,
    CAPI_DEB: CAPI_DEB_SHA1
}

from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler 

import os.path

def full_url(deb):
    return __base_dl_url + VERSION + "/" + deb

def install_deb(deb):
    import subprocess
    subprocess.check_call(['dpkg', '-i', deb])

def install():

    h = ArchiveUrlFetchHandler()

    # download, validate, install
    for deb, sha in __debs.iteritems():
        install_deb(h.download_and_validate(full_url(deb), sha, validate="sha1"))
