import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_diffOrder_getWorkPlatformOrderInfo(params=params, headers=headers):
    """
    查询工作平台货损货差单信息
    /mgmt/inventory/diffOrder/getWorkPlatformOrderInfo

    参数说明:
    - orderSn: orderSn
    """

    url = "/mgmt/inventory/diffOrder/getWorkPlatformOrderInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
