import os

from util.client import client

data = {
    "orderCompleteTime": "",  # 订单完成时间
    "orderId": 0,  # 订单ID
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_manualOrderComplete(data=data, headers=headers):
    """
    人工操作完成订单
    /mgmt/order/manualOrderComplete

    参数说明:
    - orderCompleteTime: 订单完成时间
    - orderId: 订单ID
    - remark: 备注
    """

    url = "/mgmt/order/manualOrderComplete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
