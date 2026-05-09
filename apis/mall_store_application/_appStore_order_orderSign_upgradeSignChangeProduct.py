import os

from util.client import client

data = {
    "chooseProducts": [],  # 签约3.0 可选商品集合
    "mustProducts": [],  # 签约3.0 修改必选商品集合
    "promotionId": 0,  # 活动ID
    "signNo": "",  # 签约单号
    "subOrderSignId": 0,  # 签约单子单自增ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_upgradeSignChangeProduct(data=data, headers=headers):
    """
    签约购3.0 修改签约产品
    /appStore/order/orderSign/upgradeSignChangeProduct

    参数说明:
    - chooseProducts: 签约3.0 可选商品集合
    - mustProducts: 签约3.0 修改必选商品集合
    - promotionId: 活动ID
    - signNo: 签约单号
    - subOrderSignId: 签约单子单自增ID
    """

    url = "/appStore/order/orderSign/upgradeSignChangeProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
