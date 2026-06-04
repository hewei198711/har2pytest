import os

from util.client import client

params = {
    "activityId": 0,  # activityId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_luckyActivityEditDetails(params=params, headers=headers):
    """
    抽奖活动-管理列表跳编辑
    /mgmt/prmt/luckyActivity/luckyActivityEditDetails

    参数说明:
    - activityId: activityId
    """

    url = "/mgmt/prmt/luckyActivity/luckyActivityEditDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
