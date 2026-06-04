import os

from util.client import client

params = {
    "exchangeNo": "",  # exchangeNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_getOrderExchangeDetails(params=params, headers=headers):
    """
    换货详情
    /mgmt/order/exchange/getOrderExchangeDetails

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/getOrderExchangeDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
