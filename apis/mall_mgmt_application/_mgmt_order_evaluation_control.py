import os

from util.client import client

data = {
    "displayOnFrontend": False,  # 是否前端展示
    "evaluateId": 0,  # 评价ID
    "evaluateIds": [],  # 评价ID数组
    "isDefaultEvaluation": False,  # 是否默认评价
    "isQualityEvaluation": False,  # 是否优质评价
    "isTopEvaluation": False,  # 是否评价置顶
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_control(data=data, headers=headers):
    """
    评价管控操作
    /mgmt/order/evaluation/control

    参数说明:
    - displayOnFrontend: 是否前端展示
    - evaluateId: 评价ID
    - evaluateIds: 评价ID数组
    - isDefaultEvaluation: 是否默认评价
    - isQualityEvaluation: 是否优质评价
    - isTopEvaluation: 是否评价置顶
    """

    url = "/mgmt/order/evaluation/control"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
