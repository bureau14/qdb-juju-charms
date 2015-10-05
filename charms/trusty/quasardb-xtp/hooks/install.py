# change this if needed
VERSION = "2.0/beta5"

# you may want to change this

SERVER_DEB          = "server/qdb-server_2.0.0-1.deb"
SERVER_DEB_SHA1   = "2916489fefcd8aa0b59abdbd9b8d12f01e4463cd"

UTILS_DEB           = "utils/qdb-utils_2.0.0-1.deb"
UTILS_DEB_SHA1    = "15000a746527ace2f9d4de95bc2b254105d0c927"

CAPI_DEB            = "api/c/qdb-api_2.0.0-1.deb"
CAPI_DEB_SHA1     = "e66b6e27ae19126c7ca25ea21a04fd809cb5d0f3"

# don't change this
BASE_DL_URL = "https://download.quasardb.net/quasardb/"

DEBS = { 
    SERVER_DEB: SERVER_DEB_SHA1,
    UTILS_DEB: UTILS_DEB_SHA1,
    CAPI_DEB: CAPI_DEB_SHA1
}

from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler 

import os.path

def full_url(deb):
    return BASE_DL_URL + VERSION + "/" + deb

def install_deb(deb):
    import subprocess
    subprocess.check_call(['dpkg', '-i', deb])

def install():

    h = ArchiveUrlFetchHandler()

    # download, validate, install
    for deb, sha in DEBS.iteritems():
        install_deb(h.download_and_validate(full_url(deb), sha, validate="sha1"))
