import os

from util.client import client

params = {
    "productSerialNum": "",  # productSerialNum
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_repair_checkProductSerialNum(params=params, headers=headers):
    """
    检查产品序列号/二维码
    /mgmt/order/repair/checkProductSerialNum

    参数说明:
    - productSerialNum: productSerialNum
    """

    url = "/mgmt/order/repair/checkProductSerialNum"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
