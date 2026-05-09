import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStoreShow(headers=headers):
    """
    查询店铺爱心守护池显示控制:true-显示 false-隐藏
    /appStore/order/getStoreShow
    """

    url = "/appStore/order/getStoreShow"
    with client.get(url=url, headers=headers) as r:
        return r
