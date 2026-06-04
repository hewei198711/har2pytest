import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exchangeOrder_confirmMortgageExchangeOrder(data=data, headers=headers):
    """
    后台押货换确认收货
    /mgmt/inventory/exchangeOrder/confirmMortgageExchangeOrder

    参数说明:
    - id: 换货单id
    """

    url = "/mgmt/inventory/exchangeOrder/confirmMortgageExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
