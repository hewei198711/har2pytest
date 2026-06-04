import os

from util.client import client

data = {
    "activityId": 0,  # 抽奖活动id
    "customerCard": "",  # 会员卡号
    "customerName": "",  # 会员名称
    "keyword": "",  # 搜索条件
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_promotion_export_luckyActivityDisableList(data=data, headers=headers):
    """
    抽奖活动-不可参与顾客导出
    /mgmt/promotion/export/luckyActivityDisableList

    参数说明:
    - activityId: 抽奖活动id
    - customerCard: 会员卡号
    - customerName: 会员名称
    - keyword: 搜索条件
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/promotion/export/luckyActivityDisableList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
