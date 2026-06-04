import os

from util.client import client

params = {
    "activityName": "",  # 活动名称
    "activityNumber": "",  # 活动编号
    "buyerCouponName": "",  # 购货人优惠券
    "createTimeEnd": "",  # 活动创建时间止区(yyyy-MM-dd)
    "createTimeStart": "",  # 活动创建时间起区(yyyy-MM-dd)
    "endTimeEnd": "",  # 活动结束时间止区(yyyy-MM-dd)
    "endTimeStart": "",  # 活动结束时间起区(yyyy-MM-dd)
    "handlerCouponName": "",  # 经办人优惠券
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "startTimeEnd": "",  # 活动开始时间止区(yyyy-MM-dd)
    "startTimeStart": "",  # 活动开始时间起区(yyyy-MM-dd)
    "state": 0,  # 状态:1-待审核,2-待开始,3-进行中,4-已驳回,5-草稿,6-已结束
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_shoppedGift(params=params, headers=headers):
    """
    购物有礼活动各状态数量
    /mgmt/prmt/state/shoppedGift

    参数说明:
    - activityName: 活动名称
    - activityNumber: 活动编号
    - buyerCouponName: 购货人优惠券
    - createTimeEnd: 活动创建时间止区(yyyy-MM-dd)
    - createTimeStart: 活动创建时间起区(yyyy-MM-dd)
    - endTimeEnd: 活动结束时间止区(yyyy-MM-dd)
    - endTimeStart: 活动结束时间起区(yyyy-MM-dd)
    - handlerCouponName: 经办人优惠券
    - pageNum: 当前页
    - pageSize: 每页数量
    - startTimeEnd: 活动开始时间止区(yyyy-MM-dd)
    - startTimeStart: 活动开始时间起区(yyyy-MM-dd)
    - state: 状态:1-待审核,2-待开始,3-进行中,4-已驳回,5-草稿,6-已结束
    """

    url = "/mgmt/prmt/state/shoppedGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
