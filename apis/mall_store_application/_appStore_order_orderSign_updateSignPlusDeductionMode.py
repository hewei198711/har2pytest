import os

from util.client import client

data = {
    "deductionMode": 0,  # 扣款方式，1：自主支付；2：自动扣款
    "signNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_updateSignPlusDeductionMode(data=data, headers=headers):
    """
    签约购3.0更新扣款方式
    /appStore/order/orderSign/updateSignPlusDeductionMode

    参数说明:
    - deductionMode: 扣款方式，1：自主支付；2：自动扣款
    - signNo: 签约单号
    """

    url = "/appStore/order/orderSign/updateSignPlusDeductionMode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
