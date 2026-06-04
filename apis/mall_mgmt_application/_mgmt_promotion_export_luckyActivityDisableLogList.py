import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "customerCard": "",  # 会员卡号
    "customerName": "",  # 会员姓名
    "endTime": "",  # 编辑时间结束 yyyy-MM-dd
    "mobile": "",  # 注册手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTime": "",  # 编辑时间开始 yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_promotion_export_luckyActivityDisableLogList(data=data, headers=headers):
    """
    抽奖活动-不可参与顾客编辑记录导出
    /mgmt/promotion/export/luckyActivityDisableLogList

    参数说明:
    - activityId: 活动id
    - customerCard: 会员卡号
    - customerName: 会员姓名
    - endTime: 编辑时间结束 yyyy-MM-dd
    - mobile: 注册手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTime: 编辑时间开始 yyyy-MM-dd
    """

    url = "/mgmt/promotion/export/luckyActivityDisableLogList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
