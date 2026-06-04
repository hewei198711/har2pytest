import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getRightsOrderDetail(params=params, headers=headers):
    """
    查询用户权益订单详情
    /mgmt/order/getRightsOrderDetail

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/order/getRightsOrderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
