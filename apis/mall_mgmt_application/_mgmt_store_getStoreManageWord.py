import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreManageWord(headers=headers):
    """
    服务中心提示语详情
    /mgmt/store/getStoreManageWord
    """

    url = "/mgmt/store/getStoreManageWord"
    with client.get(url=url, headers=headers) as r:
        return r
