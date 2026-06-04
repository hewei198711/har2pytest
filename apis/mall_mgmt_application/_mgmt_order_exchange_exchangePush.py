import os
from urllib.parse import urlencode

from util.client import client

data = {
    "ids": [],  # ids
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_exchange_exchangePush(data=data, headers=headers):
    """
    推送换货
    /mgmt/order/exchange/exchangePush

    参数说明:
    - ids: ids
    """

    url = "/mgmt/order/exchange/exchangePush"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
