import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "code": "",  # 门店编号
    "couponId": 0,  # 优惠券id
    "getType": 0,  # 领取方式:1-系统发券,2-券码兑换,3-门店转赠,4-用户领取,5-分享领券,6-助力领券,7-购物获券
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "platform": 0,  # 领取平台:1-APP,2-PC,4-小程序
    "realName": "",  # 真实姓名
    "shelvesChannel": 0,  # 领取入口:1-商品详情,2-领券中心,3-会议管理系统
    "state": 0,  # 使用状态1未使用2已使用3已作废4已失效5占用中6未转赠
    "transferType": 0,  # 转赠方式1指定用户2扫码领取3转发领取
    "usedPlatform": 0,  # 使用平台:1-APP,2-PC,4-小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getCouponDataPage(params=params, headers=headers):
    """
    优惠券数据统计分页查询
    /mgmt/prmt/coupon/getCouponDataPage

    参数说明:
    - cardNo: 会员卡号
    - code: 门店编号
    - couponId: 优惠券id
    - getType: 领取方式:1-系统发券,2-券码兑换,3-门店转赠,4-用户领取,5-分享领券,6-助力领券,7-购物获券
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页条数
    - platform: 领取平台:1-APP,2-PC,4-小程序
    - realName: 真实姓名
    - shelvesChannel: 领取入口:1-商品详情,2-领券中心,3-会议管理系统
    - state: 使用状态1未使用2已使用3已作废4已失效5占用中6未转赠
    - transferType: 转赠方式1指定用户2扫码领取3转发领取
    - usedPlatform: 使用平台:1-APP,2-PC,4-小程序
    """

    url = "/mgmt/prmt/coupon/getCouponDataPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
