import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "cardProvince": "",  # 领取人办卡省份
    "code": "",  # 门店编号
    "getTimeEndTime": "",  # 领取时间开始时间(yyyy-MM-dd)
    "getTimeStartTime": "",  # 领取时间开始时间(yyyy-MM-dd)
    "getType": 0,  # 领取方式:1-系统发券,2-券码兑换,3-门店转赠,4-用户领取,5-分享领券,6-助力领券,7-购物获券,8-抽奖活动,9-扫码领取,10-用户兑换,11-签到派发,12-外部系统派发,13-顾客转赠
    "ids": [],  # 优惠券ids
    "mobile": "",  # 手机号码
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "platform": 0,  # 领取平台:1-APP,2-PC,4-小程序
    "realname": "",  # 真实姓名
    "recipientCardProvince": "",  # 获赠人办卡省份
    "shelvesChannel": 0,  # 领取入口:1-商品详情,2-领券中心,3-会议管理系统
    "state": 0,  # 使用状态:1-未使用,2-已使用,3-已作废,4-已失效,5-占用中,6-未转赠,7-已转赠
    "transferType": 0,  # 转赠方式1指定用户2扫码领取3转发领取
    "usedPlatform": 0,  # 使用平台:1-APP,2-PC,4-小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_CouponBoard_exportCouponBoardMemberDetailList(data=data, headers=headers):
    """
    导出优惠券看板派发明细列表
    /mgmt/dataAdmin/CouponBoard/exportCouponBoardMemberDetailList

    参数说明:
    - cardNo: 会员卡号
    - cardProvince: 领取人办卡省份
    - code: 门店编号
    - getTimeEndTime: 领取时间开始时间(yyyy-MM-dd)
    - getTimeStartTime: 领取时间开始时间(yyyy-MM-dd)
    - getType: 领取方式:1-系统发券,2-券码兑换,3-门店转赠,4-用户领取,5-分享领券,6-助力领券,7-购物获券,8-抽奖活动,9-扫码领取,10-用户兑换,11-签到派发,12-外部系统派发,13-顾客转赠
    - ids: 优惠券ids
    - mobile: 手机号码
    - platform: 领取平台:1-APP,2-PC,4-小程序
    - realname: 真实姓名
    - recipientCardProvince: 获赠人办卡省份
    - shelvesChannel: 领取入口:1-商品详情,2-领券中心,3-会议管理系统
    - state: 使用状态:1-未使用,2-已使用,3-已作废,4-已失效,5-占用中,6-未转赠,7-已转赠
    - transferType: 转赠方式1指定用户2扫码领取3转发领取
    - usedPlatform: 使用平台:1-APP,2-PC,4-小程序
    """

    url = "/mgmt/dataAdmin/CouponBoard/exportCouponBoardMemberDetailList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
