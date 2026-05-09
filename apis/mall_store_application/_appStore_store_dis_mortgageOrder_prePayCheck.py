import os

from util.client import client

data = {
    "orderId": 0,  # 押货单id
    "orderQuery": "",  # 押货单查找辅助参数: 如果页面无法直接获取到押货单id，可以传里面其中一个参数来代替押货单id
    "oweDepositAmount": 0.0,  # 押货保证金欠额
    "payAmount": 0.0,  # 需付款(合计金额+保证金欠款)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_prePayCheck(data=data, headers=headers):
    """
    押货单支付前的金额校验
    /appStore/store/dis/mortgageOrder/prePayCheck

    参数说明:
    - orderId: 押货单id
    - orderQuery: 押货单查找辅助参数: 如果页面无法直接获取到押货单id，可以传里面其中一个参数来代替押货单id
    - oweDepositAmount: 押货保证金欠额
    - payAmount: 需付款(合计金额+保证金欠款)
    """

    url = "/appStore/store/dis/mortgageOrder/prePayCheck"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
