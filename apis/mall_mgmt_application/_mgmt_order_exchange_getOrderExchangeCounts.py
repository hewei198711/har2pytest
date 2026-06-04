import os

from util.client import client

params = {
    "creatorId": 0,  # creatorId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_getOrderExchangeCounts(params=params, headers=headers):
    """
    获取换货次数
    /mgmt/order/exchange/getOrderExchangeCounts

    参数说明:
    - creatorId: creatorId
    """

    url = "/mgmt/order/exchange/getOrderExchangeCounts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
