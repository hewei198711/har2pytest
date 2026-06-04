import os
from urllib.parse import urlencode

from util.client import client

data = {
    "evaluateDeadline": 0,  # 评价时限（天）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_evaluation_update(data=data, headers=headers):
    """
    设置评价时限
    /mgmt/order/evaluation/update

    参数说明:
    - evaluateDeadline: 评价时限（天）
    """

    url = "/mgmt/order/evaluation/update"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
