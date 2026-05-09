import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_selectPromotions(headers=headers):
    """
    查询进行中-已结束的活动列表
    /appStore/order/selectPromotions
    """

    url = "/appStore/order/selectPromotions"
    with client.get(url=url, headers=headers) as r:
        return r
