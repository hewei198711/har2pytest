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


def _mgmt_order_exchange_cancelOrderExchangeAudit(data=data, headers=headers):
    """
    撤销换货审核
    /mgmt/order/exchange/cancelOrderExchangeAudit

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/cancelOrderExchangeAudit"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
