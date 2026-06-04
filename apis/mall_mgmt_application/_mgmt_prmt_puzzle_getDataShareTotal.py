import os

from util.client import client

data = {
    "createTimeMax": "",  # 创建时间末
    "createTimeMin": "",  # 创建时间始
    "puzzleId": 0,  # 拼图活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_getDataShareTotal(data=data, headers=headers):
    """
    拼图数分享总
    /mgmt/prmt/puzzle/getDataShareTotal

    参数说明:
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - puzzleId: 拼图活动id
    """

    url = "/mgmt/prmt/puzzle/getDataShareTotal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
