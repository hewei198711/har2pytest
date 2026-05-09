import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_getWorkPlatformOrderInfo(params=params, headers=headers):
    """
    查询工作平台货损货差单信息
    /appStore/productDiff/getWorkPlatformOrderInfo

    参数说明:
    - orderSn: orderSn
    """

    url = "/appStore/productDiff/getWorkPlatformOrderInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
