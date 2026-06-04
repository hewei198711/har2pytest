import os
from urllib.parse import urlencode

from util.client import client

data = {
    "days": 0,  # days
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_setOrderInvoiceOvertimeDays(data=data, headers=headers):
    """
    运营后台-设置订单超时天数
    /mgmt/order/setOrderInvoiceOvertimeDays

    参数说明:
    - days: days
    """

    url = "/mgmt/order/setOrderInvoiceOvertimeDays"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
