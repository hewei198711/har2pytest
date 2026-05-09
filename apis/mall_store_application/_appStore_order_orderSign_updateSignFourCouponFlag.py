import os

from util.client import client

data = {
    "couponFlag": False,  # 用券标识，是：true；否：false
    "signNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_updateSignFourCouponFlag(data=data, headers=headers):
    """
    签约购4.0更新是否自动用券
    /appStore/order/orderSign/updateSignFourCouponFlag

    参数说明:
    - couponFlag: 用券标识，是：true；否：false
    - signNo: 签约单号
    """

    url = "/appStore/order/orderSign/updateSignFourCouponFlag"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
