import os

from util.client import client

data = {
    "dicType": "",  # 数据类型
    "dicValue": "",  # 数据值
    "operator": "",  # 操作人工号
    "operatorName": "",  # 操作人姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterSaleEvaluate_updateDictionary(data=data, headers=headers):
    """
    自动评价天数设置
    /mgmt/afterSaleEvaluate/updateDictionary

    参数说明:
    - dicType: 数据类型
    - dicValue: 数据值
    - operator: 操作人工号
    - operatorName: 操作人姓名
    """

    url = "/mgmt/afterSaleEvaluate/updateDictionary"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
