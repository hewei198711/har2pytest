import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间末
    "createTimeMin": "",  # 创建时间始
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionCode": "",  # 活动编码
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "promotionStates": [],  # 活动状态集合(同时查询多种状态):1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_sendGift(params=params, headers=headers):
    """
    送礼活动各状态数量
    /mgmt/prmt/state/sendGift

    参数说明:
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionCode: 活动编码
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - promotionStates: 活动状态集合(同时查询多种状态):1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    """

    url = "/mgmt/prmt/state/sendGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
