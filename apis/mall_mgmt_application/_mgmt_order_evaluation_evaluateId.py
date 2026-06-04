import os

from util.client import client

params = {
    "evaluateId": 0,  # 评价的唯一标识ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_evaluateId(params=params, headers=headers):
    """
    根据评价ID获取评价详情
    /mgmt/order/evaluation/{evaluateId}

    参数说明:
    - evaluateId: 评价的唯一标识ID
    """

    url = f"/mgmt/order/evaluation/{params['evaluateId']}"
    with client.get(url=url, headers=headers) as r:
        return r
