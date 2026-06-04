import os

from util.client import client

params = {
    "activityId": 0,  # activityId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_prizeConfigDetails(params=params, headers=headers):
    """
    抽奖活动-活动奖品详情
    /mgmt/prmt/luckyActivity/prizeConfigDetails

    参数说明:
    - activityId: activityId
    """

    url = "/mgmt/prmt/luckyActivity/prizeConfigDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
