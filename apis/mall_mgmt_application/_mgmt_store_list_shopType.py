import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_list_shopType(params=params, headers=headers):
    """
    网点类型列表
    /mgmt/store/list/shopType

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/store/list/shopType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
