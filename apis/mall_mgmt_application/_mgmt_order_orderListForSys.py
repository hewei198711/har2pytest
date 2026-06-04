import os

from util.client import client

params = {
    "receiverPhone": "",  # receiverPhone
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderListForSys(params=params, headers=headers):
    """
    指定手机号不发货-查看订单
    /mgmt/order/orderListForSys

    参数说明:
    - receiverPhone: receiverPhone
    """

    url = "/mgmt/order/orderListForSys"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
