import os

from util.client import client

data = {
    "combineId": 0,  # 套装组合id
    "combineNum": 0,  # 套装组合数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine(data=data, headers=headers):
    """
    套装组合
    /mgmt/inventory/combine

    参数说明:
    - combineId: 套装组合id
    - combineNum: 套装组合数量
    """

    url = "/mgmt/inventory/combine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
