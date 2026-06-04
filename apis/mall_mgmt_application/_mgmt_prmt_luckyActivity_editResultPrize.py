import os

from util.client import client

data = {
    "activityId": 0,  # 抽奖活动id
    "prizes": [
        {"mobileRegion": "", "mobileResultPicture": "", "npId": 0, "pcRegion": "", "pcResultPicture": "", "prizeId": 0}
    ],  # 奖品信息集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editResultPrize(data=data, headers=headers):
    """
    编辑刮刮乐抽奖结果样式
    /mgmt/prmt/luckyActivity/editResultPrize

    参数说明:
    - activityId: 抽奖活动id
    - prizes: 奖品信息集合
    - prizes.mobileRegion: 移动端刮刮乐区域配置
    - prizes.mobileResultPicture: 移动端抽奖结果图片地址(刮刮乐)
    - prizes.npId: 不中奖配置id
    - prizes.pcRegion: PC端刮刮乐区域配置
    - prizes.pcResultPicture: PC抽奖结果图片地址(刮刮乐)
    - prizes.prizeId: 中奖奖品id
    """

    url = "/mgmt/prmt/luckyActivity/editResultPrize"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
