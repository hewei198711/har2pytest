import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "productList": [],  # 购买产品信息
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_qualificationFour(data=data, headers=headers):
    """
    查询用户是否有签约购4.0活动资格
    /appStore/order/orderSign/qualificationFour

    参数说明:
    - cardNo: 会员卡号
    - productList: 购买产品信息
    - promotionId: 活动id
    """

    url = "/appStore/order/orderSign/qualificationFour"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
