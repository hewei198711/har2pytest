import os

from util.client import client

params = {
    "applyId": 0,  # applyId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_detail(params=params, headers=headers):
    """
    年审申请详情
    /appStore/store/detail

    参数说明:
    - applyId: applyId
    """

    url = "/appStore/store/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
