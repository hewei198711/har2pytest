import os

from util.client import client

data = {
    "backPicture": "",  # 主页背景图片地址
    "baseCount": 0,  # 基础拼图次数
    "diff": 0,  # 游戏难度(0-2x2 1-3x3 2-4x4)
    "endTime": "",  # 结束时间
    "everyShareGetCount": 0,  # 每次分享获得次数
    "id": 0,  # 主键id
    "luckyActivityId": 0,  # 关联的抽奖活动id
    "maxShareTimes": 0,  # 最大支持分享次数
    "memoryTime": 0,  # 记忆时长(秒)
    "pictures": [],  # 拼图图片地址集合
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "puzzleTime": 0,  # 拼图时长(秒)
    "remark": "",  # 活动规则(富文本)
    "shareGetCount": False,  # 是否支持分享获得次数 false-否 true-是
    "startTime": "",  # 开始时间
    "wxSharePicture": "",  # 小程序分享卡片图片地址
    "wxShareRemark": "",  # 小程序分享卡片文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_edit(data=data, headers=headers):
    """
    编辑活动
    /mgmt/prmt/puzzle/edit

    参数说明:
    - backPicture: 主页背景图片地址
    - baseCount: 基础拼图次数
    - diff: 游戏难度(0-2x2 1-3x3 2-4x4)
    - endTime: 结束时间
    - everyShareGetCount: 每次分享获得次数
    - id: 主键id
    - luckyActivityId: 关联的抽奖活动id
    - maxShareTimes: 最大支持分享次数
    - memoryTime: 记忆时长(秒)
    - pictures: 拼图图片地址集合
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - puzzleTime: 拼图时长(秒)
    - remark: 活动规则(富文本)
    - shareGetCount: 是否支持分享获得次数 false-否 true-是
    - startTime: 开始时间
    - wxSharePicture: 小程序分享卡片图片地址
    - wxShareRemark: 小程序分享卡片文案
    """

    url = "/mgmt/prmt/puzzle/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
