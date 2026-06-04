import os

from util.client import client

data = {
    "plateConfigList": [
        {"activityId": 0, "luckyRate": 0.0, "npId": 0, "plateId": 0, "positionNumber": 0, "prizeId": 0}
    ],  # 奖盘配置
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editPlateConfigLuckyRate(data=data, headers=headers):
    """
    活动奖品-奖盘编辑-奖品抽奖概率
    /mgmt/prmt/luckyActivity/editPlateConfigLuckyRate

    参数说明:
    - plateConfigList: 奖盘配置
    - plateConfigList.activityId: 活动id
    - plateConfigList.luckyRate: 抽奖概率
    - plateConfigList.npId: 不中奖配置id
    - plateConfigList.plateId: id标识
    - plateConfigList.positionNumber: 奖盘位置号
    - plateConfigList.prizeId: 奖品id
    """

    url = "/mgmt/prmt/luckyActivity/editPlateConfigLuckyRate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
