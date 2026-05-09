import os
from urllib.parse import urlencode

from util.client import client

data = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_purchaseExchangeOrder_product(data=data, headers=headers):
    """
    获取换货产品信息
    /appStore/purchaseExchangeOrder/product

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/purchaseExchangeOrder/product"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
