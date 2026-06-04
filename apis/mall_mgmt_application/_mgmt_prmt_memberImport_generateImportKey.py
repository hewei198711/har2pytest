import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_memberImport_generateImportKey(headers=headers):
    """
    生成importKey
    /mgmt/prmt/memberImport/generateImportKey
    """

    url = "/mgmt/prmt/memberImport/generateImportKey"
    with client.get(url=url, headers=headers) as r:
        return r
