import os

from util.client import client

params = {
    "repairNo": "",  # repairNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_repair_detail(params=params, headers=headers):
    """
    获取维修单详情
    /appStore/order/repair/detail

    参数说明:
    - repairNo: repairNo
    """

    url = "/appStore/order/repair/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
