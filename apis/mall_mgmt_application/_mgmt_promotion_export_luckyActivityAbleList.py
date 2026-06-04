import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "customerCard": "",  # 会员卡号
    "customerName": "",  # 会员姓名
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "state": 0,  # 状态(0:禁用；1：启用)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_promotion_export_luckyActivityAbleList(data=data, headers=headers):
    """
    抽奖活动-活动顾客导出
    /mgmt/promotion/export/luckyActivityAbleList

    参数说明:
    - activityId: 活动id
    - customerCard: 会员卡号
    - customerName: 会员姓名
    - mobile: 注册手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - state: 状态(0:禁用；1：启用)
    """

    url = "/mgmt/promotion/export/luckyActivityAbleList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
