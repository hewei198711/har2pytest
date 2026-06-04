import os

from util.client import client

params = {
    "passwordId": 0,  # passwordId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_selectLuckyList(params=params, headers=headers):
    """
    查询口令活动所关联的抽奖活动id集合
    /mgmt/prmt/luckyActivity/selectLuckyList

    参数说明:
    - passwordId: passwordId
    """

    url = "/mgmt/prmt/luckyActivity/selectLuckyList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
