import os

from util.client import client

params = {
    "customerId": "",  # customerId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getUpgradeOrderList(params=params, headers=headers):
    """
    查询用户可升级订单列表
    /mgmt/order/getUpgradeOrderList

    参数说明:
    - customerId: customerId
    """

    url = "/mgmt/order/getUpgradeOrderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
