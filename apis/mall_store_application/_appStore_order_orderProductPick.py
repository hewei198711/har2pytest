import os

from util.client import client

data = {
    "allIdList": [],  # 所有产品ID列表
    "orderId": 0,  # 订单ID
    "pickIdList": [],  # 已选产品ID列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderProductPick(data=data, headers=headers):
    """
    产品信息-拣货标识接口
    /appStore/order/orderProductPick

    参数说明:
    - allIdList: 所有产品ID列表
    - orderId: 订单ID
    - pickIdList: 已选产品ID列表
    """

    url = "/appStore/order/orderProductPick"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
