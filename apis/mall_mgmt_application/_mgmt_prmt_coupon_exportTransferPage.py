import os

from util.client import client

params = {
    "cardNo": "",  # 转赠顾客会员卡号
    "couponId": 0,  # 优惠券id
    "createTimeEnd": "",  # 转赠时间止(yyyy-MM-dd)
    "createTimeStart": "",  # 转赠时间起(yyyy-MM-dd)
    "mobile": "",  # 转赠顾客手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "realName": "",  # 转赠顾客姓名
    "receiveTimeEnd": "",  # 领取时间止(yyyy-MM-dd)
    "receiveTimeStart": "",  # 领取时间起(yyyy-MM-dd)
    "recipientCardNo": "",  # 获赠顾客会员卡号
    "recipientMobile": "",  # 获赠顾客手机号
    "recipientRealName": "",  # 获赠顾客姓名
    "state": 0,  # 优惠券状态 1-未使用,2-已使用,3-已作废,4-已失效,5-占用中
    "transferType": 0,  # 转赠方式:1-指定用户,2-扫码领取,3-微信领取
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_exportTransferPage(params=params, headers=headers):
    """
    导出优惠券转赠详情
    /mgmt/prmt/coupon/exportTransferPage

    参数说明:
    - cardNo: 转赠顾客会员卡号
    - couponId: 优惠券id
    - createTimeEnd: 转赠时间止(yyyy-MM-dd)
    - createTimeStart: 转赠时间起(yyyy-MM-dd)
    - mobile: 转赠顾客手机号
    - pageNum: 当前页
    - pageSize: 每页条数
    - realName: 转赠顾客姓名
    - receiveTimeEnd: 领取时间止(yyyy-MM-dd)
    - receiveTimeStart: 领取时间起(yyyy-MM-dd)
    - recipientCardNo: 获赠顾客会员卡号
    - recipientMobile: 获赠顾客手机号
    - recipientRealName: 获赠顾客姓名
    - state: 优惠券状态 1-未使用,2-已使用,3-已作废,4-已失效,5-占用中
    - transferType: 转赠方式:1-指定用户,2-扫码领取,3-微信领取
    """

    url = "/mgmt/prmt/coupon/exportTransferPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
