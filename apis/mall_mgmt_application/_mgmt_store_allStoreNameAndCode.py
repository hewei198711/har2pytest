import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_allStoreNameAndCode(headers=headers):
    """
    获取所有服务中心code和name
    /mgmt/store/allStoreNameAndCode
    """

    url = "/mgmt/store/allStoreNameAndCode"
    with client.get(url=url, headers=headers) as r:
        return r
