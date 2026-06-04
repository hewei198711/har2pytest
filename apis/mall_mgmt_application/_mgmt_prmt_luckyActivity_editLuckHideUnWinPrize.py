import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "hideUnwinStatus": 0,  # 前台隐藏未中奖信息 1、开启  2、关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editLuckHideUnWinPrize(data=data, headers=headers):
    """
    编辑-前台隐藏未中奖信息
    /mgmt/prmt/luckyActivity/editLuckHideUnWinPrize

    参数说明:
    - activityId: 活动id
    - hideUnwinStatus: 前台隐藏未中奖信息 1、开启  2、关闭
    """

    url = "/mgmt/prmt/luckyActivity/editLuckHideUnWinPrize"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
