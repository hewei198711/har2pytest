import os

from util.client import client

data = {
    "activityName": "",  # 活动名称
    "activityNumber": "",  # 活动编号
    "buyerCoupons": [{"couponId": 0, "getCount": 0}],  # 购货人关联优惠券
    "buyerGetCoupon": False,  # 购货人是否获券
    "endTime": "",  # 结束时间
    "grantBuyer": 0,  # 购货人优惠券派发时间:1-即时派发,2-订单支付后定时派发,3-每月定时派发
    "grantBuyerDays": 0,  # 购货人优惠券派发时间设值
    "grantHandler": 0,  # 经办人优惠券派发时间:1-即时派发,2-订单支付后定时派发,3-每月定时派发
    "grantHandlerDays": 0,  # 经办人优惠券派发时间设值
    "handlerCoupons": [{"couponId": 0, "getCount": 0}],  # 经办人关联优惠券
    "handlerGetCoupon": False,  # 经办人是否获券
    "id": 0,  # 活动主键
    "offShelves": 0,  # 下架方式:1-定时下架,2-不限时
    "productRange": 0,  # 产品适用范围:2-指定适用产品
    "remarks": "",  # 活动说明
    "serialNos": [],  # 产品编码集合
    "shelves": 0,  # 上架方式:1-定时上架,2-即时上架
    "startTime": "",  # 开始时间
    "state": 0,  # 状态:1-待审核,5-草稿
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_edit(data=data, headers=headers):
    """
    编辑购物有礼活动
    /mgmt/prmt/shoppedGift/edit

    参数说明:
    - activityName: 活动名称
    - activityNumber: 活动编号
    - buyerCoupons: 购货人关联优惠券
    - buyerCoupons.couponId: 优惠券id
    - buyerCoupons.getCount: 派发数量
    - buyerGetCoupon: 购货人是否获券
    - endTime: 结束时间
    - grantBuyer: 购货人优惠券派发时间:1-即时派发,2-订单支付后定时派发,3-每月定时派发
    - grantBuyerDays: 购货人优惠券派发时间设值
    - grantHandler: 经办人优惠券派发时间:1-即时派发,2-订单支付后定时派发,3-每月定时派发
    - grantHandlerDays: 经办人优惠券派发时间设值
    - handlerCoupons: 经办人关联优惠券
    - handlerCoupons.couponId: 优惠券id
    - handlerCoupons.getCount: 派发数量
    - handlerGetCoupon: 经办人是否获券
    - id: 活动主键
    - offShelves: 下架方式:1-定时下架,2-不限时
    - productRange: 产品适用范围:2-指定适用产品
    - remarks: 活动说明
    - serialNos: 产品编码集合
    - shelves: 上架方式:1-定时上架,2-即时上架
    - startTime: 开始时间
    - state: 状态:1-待审核,5-草稿
    """

    url = "/mgmt/prmt/shoppedGift/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
