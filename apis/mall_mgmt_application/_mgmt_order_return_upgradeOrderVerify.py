import os
from urllib.parse import urlencode

from util.client import client

data = {
    "applySource": 0,  # applySource
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_return_upgradeOrderVerify(data=data, headers=headers):
    """
    升级单校验
    /mgmt/order/return/upgradeOrderVerify

    参数说明:
    - applySource: applySource
    - orderNo: orderNo
    """

    url = "/mgmt/order/return/upgradeOrderVerify"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
