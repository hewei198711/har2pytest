import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_detail(params=params, headers=headers):
    """
    店铺运营系统-签约购管理列表-详情
    /appStore/order/orderSign/detail

    参数说明:
    - signNo: signNo
    """

    url = "/appStore/order/orderSign/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
