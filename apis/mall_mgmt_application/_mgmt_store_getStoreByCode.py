import os

from util.client import client

params = {
    "code": "",  # code
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreByCode(params=params, headers=headers):
    """
    根据服务中心编号获取服务中心
    /mgmt/store/getStoreByCode

    参数说明:
    - code: code
    """

    url = "/mgmt/store/getStoreByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
