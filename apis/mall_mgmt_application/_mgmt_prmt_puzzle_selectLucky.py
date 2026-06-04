import os

from util.client import client

params = {
    "activityCode": "",  # 抽奖活动编码
    "activityName": "",  # 抽奖活动名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_selectLucky(params=params, headers=headers):
    """
    查询符合条件的抽奖活动
    /mgmt/prmt/puzzle/selectLucky

    参数说明:
    - activityCode: 抽奖活动编码
    - activityName: 抽奖活动名称
    """

    url = "/mgmt/prmt/puzzle/selectLucky"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
