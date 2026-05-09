import os

from util.client import client

data = {
    "itemAttitude": 0,  # 评价项-服务态度 1不满意 2一般 3满意 4非常满意
    "itemConvenience": 0,  # 评价项-服务便捷度 1不满意 2一般 3满意 4非常满意
    "itemLogistics": 0,  # 评价项-售后物流评价 1不满意 2一般 3满意 4非常满意
    "itemTimeliness": 0,  # 评价项-服务时效 1不满意 2一般 3满意 4非常满意
    "orderSn": "",  # 押货售后单号
    "orderType": 0,  # 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_afterMortgage_satisfaction_evaluate(data=data, headers=headers):
    """
    评价
    /appStore/afterMortgage/satisfaction/evaluate

    参数说明:
    - itemAttitude: 评价项-服务态度 1不满意 2一般 3满意 4非常满意
    - itemConvenience: 评价项-服务便捷度 1不满意 2一般 3满意 4非常满意
    - itemLogistics: 评价项-售后物流评价 1不满意 2一般 3满意 4非常满意
    - itemTimeliness: 评价项-服务时效 1不满意 2一般 3满意 4非常满意
    - orderSn: 押货售后单号
    - orderType: 押货售后单类型 1->1:3押货退货 2->1:3押货换货 3->1:3货损货差 4->85押货退货 5->85押货换货 6->85货损货差
    """

    url = "/appStore/afterMortgage/satisfaction/evaluate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
