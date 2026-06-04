import os

from util.client import client

data = {
    "createTimeMax": "",  # 创建时间止
    "createTimeMin": "",  # 创建时间起
    "endTimeMax": "",  # 活动结束时间止
    "endTimeMin": "",  # 活动结束时间起
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionCode": "",  # 活动编码
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "promotionType": 0,  # 活动类型:1-抢购活动 2-常规活动 3-换购活动 4-3S活动 5-随心购活动 6-签约购4.0 7-抽奖活动 8-购物有礼 9-口令活动10-赠品兑换活动管理 11-送礼活动 12-拼图活动 13-优惠券管理列表 14-优惠券派发管理列表  15-优惠券券包派发管理列表 16-转赠优惠券派发管理列表 17-登录提醒列表 18-领券中心管理列表 19-分享领券管理列表 20-公益购活动
    "startTimeMax": "",  # 活动开始时间止
    "startTimeMin": "",  # 活动开始时间起
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_data(data=data, headers=headers):
    """
    分页查询活动看板数据
    /mgmt/prmt/monthly/data

    参数说明:
    - createTimeMax: 创建时间止
    - createTimeMin: 创建时间起
    - endTimeMax: 活动结束时间止
    - endTimeMin: 活动结束时间起
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionCode: 活动编码
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - promotionType: 活动类型:1-抢购活动 2-常规活动 3-换购活动 4-3S活动 5-随心购活动 6-签约购4.0 7-抽奖活动 8-购物有礼 9-口令活动10-赠品兑换活动管理 11-送礼活动 12-拼图活动 13-优惠券管理列表 14-优惠券派发管理列表  15-优惠券券包派发管理列表 16-转赠优惠券派发管理列表 17-登录提醒列表 18-领券中心管理列表 19-分享领券管理列表 20-公益购活动
    - startTimeMax: 活动开始时间止
    - startTimeMin: 活动开始时间起
    """

    url = "/mgmt/prmt/monthly/data"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
