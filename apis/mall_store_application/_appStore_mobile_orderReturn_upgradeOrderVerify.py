import os
from urllib.parse import urlencode

from util.client import client

data = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_mobile_orderReturn_upgradeOrderVerify(data=data, headers=headers):
    """
    升级单校验
    /appStore/mobile/orderReturn/upgradeOrderVerify

    参数说明:
    - orderNo: orderNo
    """

    url = "/appStore/mobile/orderReturn/upgradeOrderVerify"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
