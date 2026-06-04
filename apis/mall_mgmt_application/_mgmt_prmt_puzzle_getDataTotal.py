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


def _mgmt_prmt_puzzle_getDataTotal(data=data, headers=headers):
    """
    拼图数据统计总
    /mgmt/prmt/puzzle/getDataTotal

    参数说明:
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - puzzleId: 拼图活动id
    """

    url = "/mgmt/prmt/puzzle/getDataTotal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
