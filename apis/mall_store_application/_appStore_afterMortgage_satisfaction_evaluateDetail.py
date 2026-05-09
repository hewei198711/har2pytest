import os

from util.client import client

params = {
    "orderSn": "",  # 售后单编号
    "orderType": 0,  # 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_afterMortgage_satisfaction_evaluateDetail(params=params, headers=headers):
    """
    获取评价详情
    /appStore/afterMortgage/satisfaction/evaluateDetail

    参数说明:
    - orderSn: 售后单编号
    - orderType: 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
    """

    url = "/appStore/afterMortgage/satisfaction/evaluateDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
