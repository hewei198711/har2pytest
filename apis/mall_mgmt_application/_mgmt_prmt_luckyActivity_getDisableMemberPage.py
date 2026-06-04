import os

from util.client import client

params = {
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


def _mgmt_prmt_luckyActivity_getDisableMemberPage(params=params, headers=headers):
    """
    分页查询不可参加顾客
    /mgmt/prmt/luckyActivity/getDisableMemberPage

    参数说明:
    - activityId: 抽奖活动id
    - customerCard: 会员卡号
    - customerName: 会员名称
    - keyword: 搜索条件
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/luckyActivity/getDisableMemberPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
