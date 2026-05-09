import os

from util.client import client

params = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_clauseAndCommitment(params=params, headers=headers):
    """
    获取签约购4.0活动条款与代购承诺书
    /appStore/complex/clauseAndCommitment

    参数说明:
    - id: 活动id
    """

    url = "/appStore/complex/clauseAndCommitment"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
