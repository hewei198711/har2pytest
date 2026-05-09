import os
from urllib.parse import urlencode

from util.client import client

data = {
    "storeCode": "",  # storeCode
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_web_store_refund_getMaxRefundAmount(data=data, headers=headers):
    """
    获取退款可退最大金额
    /appStore/web/store/refund/getMaxRefundAmount

    参数说明:
    - storeCode: storeCode
    - type: type
    """

    url = "/appStore/web/store/refund/getMaxRefundAmount"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
