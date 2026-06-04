import os

from util.client import client

params = {
    "exchangeNo": "",  # exchangeNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_getOrderExchangeUpdateInfo(params=params, headers=headers):
    """
    获取换货修改信息
    /mgmt/order/exchange/getOrderExchangeUpdateInfo

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/getOrderExchangeUpdateInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
