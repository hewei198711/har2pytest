import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "blindBoxRemark": "",  # 盲盒模式奖品文案
    "npId": 0,  # 不中奖奖品id
    "prizeId": 0,  # 中奖奖品id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_updatePrizeBlindBoxRemark(data=data, headers=headers):
    """
    修改奖品海报文案
    /mgmt/prmt/luckyActivity/updatePrizeBlindBoxRemark

    参数说明:
    - activityId: 活动id
    - blindBoxRemark: 盲盒模式奖品文案
    - npId: 不中奖奖品id
    - prizeId: 中奖奖品id
    """

    url = "/mgmt/prmt/luckyActivity/updatePrizeBlindBoxRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
