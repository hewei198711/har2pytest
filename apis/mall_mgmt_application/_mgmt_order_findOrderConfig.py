import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_findOrderConfig(headers=headers):
    """
    订单管理-修改收货次数查询
    /mgmt/order/findOrderConfig
    """

    url = "/mgmt/order/findOrderConfig"
    with client.get(url=url, headers=headers) as r:
        return r
