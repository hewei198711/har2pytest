import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getBranComByType(headers=headers):
    """
    getBranComByType
    /mgmt/sys/getBranComByType
    """

    url = "/mgmt/sys/getBranComByType"
    with client.get(url=url, headers=headers) as r:
        return r
