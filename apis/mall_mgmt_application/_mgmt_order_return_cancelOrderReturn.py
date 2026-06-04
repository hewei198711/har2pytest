import os
from urllib.parse import urlencode

from util.client import client

data = {
    "returnNo": "",  # returnNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_return_cancelOrderReturn(data=data, headers=headers):
    """
    取消退货申请
    /mgmt/order/return/cancelOrderReturn

    参数说明:
    - returnNo: returnNo
    """

    url = "/mgmt/order/return/cancelOrderReturn"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
