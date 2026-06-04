import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_cancelExchangeOrder(data=data, headers=headers):
    """
    后台押货换货取消
    /mgmt/inventory/exchangeOrder/cancelExchangeOrder

    参数说明:
    - id: 换货单id
    """

    url = "/mgmt/inventory/exchangeOrder/cancelExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
