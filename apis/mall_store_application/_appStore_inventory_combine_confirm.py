import os
from urllib.parse import urlencode

from util.client import client

data = {
    "combineId": 0,  # 套装组合id
    "combineNum": 0,  # 套装组合数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_inventory_combine_confirm(data=data, headers=headers):
    """
    确认套装组合
    /appStore/inventory/combine/confirm

    参数说明:
    - combineId: 套装组合id
    - combineNum: 套装组合数量
    """

    url = "/appStore/inventory/combine/confirm"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
