import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "code": "",  # 门店编号
    "getTimeEndTime": "",  # 领取时间开始时间(yyyy-MM-dd)
    "getTimeStartTime": "",  # 领取时间开始时间(yyyy-MM-dd)
    "ids": [],  # 优惠券ids
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "realname": "",  # 真实姓名
    "state": 0,  # 使用状态1未使用2已使用3已作废4已失效5占用中
    "transferType": 0,  # 转赠方式1指定用户2扫码领取3转发领取
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_CouponBoard_getCouponBoardTransferDetailList(data=data, headers=headers):
    """
    获取优惠券看板-转增优惠券派发明细列表
    /mgmt/dataAdmin/CouponBoard/getCouponBoardTransferDetailList

    参数说明:
    - cardNo: 会员卡号
    - code: 门店编号
    - getTimeEndTime: 领取时间开始时间(yyyy-MM-dd)
    - getTimeStartTime: 领取时间开始时间(yyyy-MM-dd)
    - ids: 优惠券ids
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页条数
    - realname: 真实姓名
    - state: 使用状态1未使用2已使用3已作废4已失效5占用中
    - transferType: 转赠方式1指定用户2扫码领取3转发领取
    """

    url = "/mgmt/dataAdmin/CouponBoard/getCouponBoardTransferDetailList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
