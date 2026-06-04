import os

from util.client import client

params = {
    "name": "",  # name
    "remark": "",  # remark
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_add_shopType(params=params, headers=headers):
    """
    添加网点类型
    /mgmt/store/add/shopType

    参数说明:
    - name: name
    - remark: remark
    """

    url = "/mgmt/store/add/shopType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
