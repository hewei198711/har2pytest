import os
from urllib.parse import urlencode

from util.client import client

data = {
    "orderMonths": [],  # orderMonths
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_order_getOrderProductSummary(data=data, headers=headers):
    """
    各系列产品业绩统汇总计表
    /appStore/order/getOrderProductSummary

    参数说明:
    - orderMonths: orderMonths
    """

    url = "/appStore/order/getOrderProductSummary"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
