import os

from util.client import client

data = {
    "feedback": "",  # 回访情况
    "id": 0,  # 售后评价id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterMortgage_satisfaction_feedback(data=data, headers=headers):
    """
    添加回访情况
    /mgmt/afterMortgage/satisfaction/feedback

    参数说明:
    - feedback: 回访情况
    - id: 售后评价id
    """

    url = "/mgmt/afterMortgage/satisfaction/feedback"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
