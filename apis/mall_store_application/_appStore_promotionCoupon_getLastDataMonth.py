import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_promotionCoupon_getLastDataMonth(headers=headers):
    """
    获取最后导入达标月份
    /appStore/promotionCoupon/getLastDataMonth
    """

    url = "/appStore/promotionCoupon/getLastDataMonth"
    with client.get(url=url, headers=headers) as r:
        return r
