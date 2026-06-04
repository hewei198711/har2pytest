import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_countStore(headers=headers):
    """
    统计有多少服务中心
    /mgmt/store/countStore
    """

    url = "/mgmt/store/countStore"
    with client.get(url=url, headers=headers) as r:
        return r
