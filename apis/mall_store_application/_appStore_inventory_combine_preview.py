import os

from util.client import client

params = {
    "combineNum": 0,  # 套装组合数量
    "id": 0,  # 套装组合id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_combine_preview(params=params, headers=headers):
    """
    套装组合预览
    /appStore/inventory/combine/preview

    参数说明:
    - combineNum: 套装组合数量
    - id: 套装组合id
    """

    url = "/appStore/inventory/combine/preview"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
