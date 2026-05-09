import os

from util.client import client

data = {
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStoreGygGuardTotal(data=data, headers=headers):
    """
    店铺运营系统-爱心守护池
    /appStore/order/getStoreGygGuardTotal

    参数说明:
    - promotionId: 活动id
    """

    url = "/appStore/order/getStoreGygGuardTotal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
