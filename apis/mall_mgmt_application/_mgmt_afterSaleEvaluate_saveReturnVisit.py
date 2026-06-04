import os

from util.client import client

data = {
    "id": 0,  # 售后评价id
    "returnVisitOperator": "",  # 回访操作人
    "returnVisitOperatorName": "",  # 回访操作人名字
    "returnVisitRemark": "",  # 回访情况
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterSaleEvaluate_saveReturnVisit(data=data, headers=headers):
    """
    回访确认/回访修改
    /mgmt/afterSaleEvaluate/saveReturnVisit

    参数说明:
    - id: 售后评价id
    - returnVisitOperator: 回访操作人
    - returnVisitOperatorName: 回访操作人名字
    - returnVisitRemark: 回访情况
    """

    url = "/mgmt/afterSaleEvaluate/saveReturnVisit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
