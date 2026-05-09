import os

from util.client import client

data = {
    "addressId": 0,  # 收货地址id
    "appStoreFlag": False,  # 签约购4.0使用，是否APP店铺，是：true；否：false
    "comboWay": 0,  # 签约购4.0使用，组合方式 0->固定组合 1->自由组合
    "couponFlag": False,  # 签约购4.0使用，是否自动用券，是：true；否：false
    "customerCard": "",  # 给某个顾客下单的会员卡号
    "customerId": 0,  # 给某个顾客下单的会员ID
    "deductionMode": 0,  # 签约购3.0、4.0使用，扣款方式，1：自主支付；2：自动扣款
    "deliverWay": 0,  # 交付方式 0-空, 1-公司交付,2-门店交付,99-全选
    "expressAmount": 0.0,  # 运费
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "giftCouponAmount": 0.0,  # 电子礼券(总计)
    "isUpgrade": 0,  # 是否需要升级 0->否 1->是
    "orderAmount": 0.0,  # 订单金额(总计)
    "orderClient": 0,  # 订单客户来源，1-PC店铺
    "orders": [],  # 每个月订单信息
    "ownerId": 0,  # 送货人ID
    "payType": 0,  # 付款方式，1->一次性付款 2->分期付款
    "promotionId": 0,  # 活动ID
    "pv": 0.0,  # 积分(PV)(总计)
    "remarks": "",  # 备注
    "secCouponAmount": 0.0,  # 使用购物秒返券金额(总计)
    "sharerId": 0,  # 分享人id
    "signType": 0,  # 签约类型，1：2.0；2：3.0；3：4.0
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_signCommit(data=data, headers=headers):
    """
    签约购提交订单
    /appStore/order/orderSign/signCommit

    参数说明:
    - addressId: 收货地址id
    - appStoreFlag: 签约购4.0使用，是否APP店铺，是：true；否：false
    - comboWay: 签约购4.0使用，组合方式 0->固定组合 1->自由组合
    - couponFlag: 签约购4.0使用，是否自动用券，是：true；否：false
    - customerCard: 给某个顾客下单的会员卡号
    - customerId: 给某个顾客下单的会员ID
    - deductionMode: 签约购3.0、4.0使用，扣款方式，1：自主支付；2：自动扣款
    - deliverWay: 交付方式 0-空, 1-公司交付,2-门店交付,99-全选
    - expressAmount: 运费
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - giftCouponAmount: 电子礼券(总计)
    - isUpgrade: 是否需要升级 0->否 1->是
    - orderAmount: 订单金额(总计)
    - orderClient: 订单客户来源，1-PC店铺
    - orders: 每个月订单信息
    - ownerId: 送货人ID
    - payType: 付款方式，1->一次性付款 2->分期付款
    - promotionId: 活动ID
    - pv: 积分(PV)(总计)
    - remarks: 备注
    - secCouponAmount: 使用购物秒返券金额(总计)
    - sharerId: 分享人id
    - signType: 签约类型，1：2.0；2：3.0；3：4.0
    - storeCode: 服务中心编码
    """

    url = "/appStore/order/orderSign/signCommit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
