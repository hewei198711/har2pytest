import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单号列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_checkDeliverSnList(params=params, headers=headers):
    """
    校验发货单号是否属于当前服务中心, 并返回不属于当前服务中心的发货单号
    /appStore/productDiff/checkDeliverSnList

    参数说明:
    - deliverSnList: 发货单号列表
    """

    url = "/appStore/productDiff/checkDeliverSnList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
