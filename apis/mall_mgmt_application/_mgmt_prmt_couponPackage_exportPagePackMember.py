import os

from util.client import client

params = {
    "alike": 0,  # 手机号是否一致:否-0 是-1
    "createAccount": "",  # SCRM活动创建人企微账号
    "createName": "",  # SCRM活动创建人名称
    "grantId": 0,  # 优惠券包派发任务id
    "luckyCard": "",  # 中奖人卡号
    "luckyMobile": "",  # 中奖人手机号
    "packNumber": "",  # 优惠券包编码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionName": "",  # SCRM活动名称
    "realReceiveCar": "",  # 领奖会员卡号
    "realReceiveMobile": "",  # 领奖手机号
    "receiveCard": "",  # 兑换卡号
    "receiveMobile": "",  # 兑换手机号
    "receiveName": "",  # 领奖会员姓名
    "receiveTimeEnd": "",  # 领奖时间止
    "receiveTimeStart": "",  # 领奖时间起
    "state": 0,  # 使用状态:1-未使用,2-已使用,3-已作废,4-已失效,5-占用中,6-未转赠,7-已转赠
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_exportPagePackMember(params=params, headers=headers):
    """
    导出优惠券详情数据明细
    /mgmt/prmt/couponPackage/exportPagePackMember

    参数说明:
    - alike: 手机号是否一致:否-0 是-1
    - createAccount: SCRM活动创建人企微账号
    - createName: SCRM活动创建人名称
    - grantId: 优惠券包派发任务id
    - luckyCard: 中奖人卡号
    - luckyMobile: 中奖人手机号
    - packNumber: 优惠券包编码
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionName: SCRM活动名称
    - realReceiveCar: 领奖会员卡号
    - realReceiveMobile: 领奖手机号
    - receiveCard: 兑换卡号
    - receiveMobile: 兑换手机号
    - receiveName: 领奖会员姓名
    - receiveTimeEnd: 领奖时间止
    - receiveTimeStart: 领奖时间起
    - state: 使用状态:1-未使用,2-已使用,3-已作废,4-已失效,5-占用中,6-未转赠,7-已转赠
    """

    url = "/mgmt/prmt/couponPackage/exportPagePackMember"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
