import os
from urllib.parse import urlencode

from util.client import client

data = {
    "exchangeNo": "",  # exchangeNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_exchange_cancelOrderExchange(data=data, headers=headers):
    """
    取消换货申请
    /mgmt/order/exchange/cancelOrderExchange

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/cancelOrderExchange"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
