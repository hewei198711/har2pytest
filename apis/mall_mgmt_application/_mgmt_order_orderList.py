import os

from util.client import client

params = {
    "balancePayEndTime": "",  # 尾款支付结束时间
    "balancePayStartTime": "",  # 尾款支付开始时间
    "businessMode": 0,  # 经营模式 1->1:3押货 2->85折押货
    "commitEndTime": "",  # 开单结束时间
    "commitStartTime": "",  # 开单开始时间
    "companyCodes": "",  # 分公司编号，多个用逗号分隔
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客会员卡
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerTypes": "",  # 顾客类型，多个用英文逗号分隔 1->普通顾客 2->优惠顾客 3->微店 4->云商
    "depositNo": "",  # 定金单号
    "depositPayEndTime": "",  # 定金支付结束时间
    "depositPayStartTime": "",  # 定金支付开始时间
    "discountLevelList": [],  # 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    "evaluate": "",  # 评价 0->未评价 1->不满意 2-> 满意 3->非常满意
    "evaluates": "",  # 评价，多个用英文逗号分隔 0->未评价 1->不满意 2-> 满意 3->非常满意
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送 3->体验中心自提 4->微信小店交付
    "financeCompanyCodes": "",  # 财务分公司编号，多个用逗号分隔
    "from": 0,  # TODO: 添加参数说明
    "isDeliver": 0,  # 订单是否需要发货 0->不发货 1->发货
    "isDisSelfStoreOrder": 0,  # 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    "isInvoice": 0,  # 是否开票 0->否 1->是
    "isPrivacy": 0,  # 是否开启隐私保护 0->否 1->是
    "isPromotion": 0,  # 是否活动 0->否 1->是
    "isReply": 0,  # 是否回复 0->未回复 1->已回复
    "isUpgrade": 0,  # 是否升级单
    "loginSource": "",  # 登录渠道 health->上海健康 ev->企业微信 skin -> 精准护肤
    "orderMonth": "",  # 业绩月份yyyyMM
    "orderNo": "",  # 订单编号
    "orderStatus": 0,  # 订单状态 -5->待收礼 -4->活动押货待支付 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "orderStatusList": [],  # 订单状态 -5->待收礼 -4->活动押货待支付 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "orderTypes": "",  # 订单类型，多个用英文逗号分隔 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9->签约购转分订单 10->配件订单 11->体验中心自提订单 12->礼物订单 13->微信小店转分订单
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "productOrderTypes": "",  # 订货类型，多个用英文逗号分隔 1->产品订货 2->资料订货 3->订制品订货
    "productTypes": "",  # 商品类型，多个用英文逗号分隔 1->普通商品 2->定制商品 3->组合商品
    "receiverPhone": "",  # 收货人手机号
    "serialNo": "",  # 产品编码
    "sources": "",  # 来源，多个用英文逗号分隔 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0 6->运营后台
    "stockTypes": "",  # 库存类型，多个用英文逗号分隔 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    "storeCancel": 0,  # 是否结点变更  0->否 1->是
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderList(params=params, headers=headers):
    """
    订单列表
    /mgmt/order/orderList

    参数说明:
    - balancePayEndTime: 尾款支付结束时间
    - balancePayStartTime: 尾款支付开始时间
    - businessMode: 经营模式 1->1:3押货 2->85折押货
    - commitEndTime: 开单结束时间
    - commitStartTime: 开单开始时间
    - companyCodes: 分公司编号，多个用逗号分隔
    - creatorCard: 开单人卡号
    - customerCard: 顾客会员卡
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerTypes: 顾客类型，多个用英文逗号分隔 1->普通顾客 2->优惠顾客 3->微店 4->云商
    - depositNo: 定金单号
    - depositPayEndTime: 定金支付结束时间
    - depositPayStartTime: 定金支付开始时间
    - discountLevelList: 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    - evaluate: 评价 0->未评价 1->不满意 2-> 满意 3->非常满意
    - evaluates: 评价，多个用英文逗号分隔 0->未评价 1->不满意 2-> 满意 3->非常满意
    - expressType: 配送方式 1->服务中心自提 2->公司配送 3->体验中心自提 4->微信小店交付
    - financeCompanyCodes: 财务分公司编号，多个用逗号分隔
    - isDeliver: 订单是否需要发货 0->不发货 1->发货
    - isDisSelfStoreOrder: 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    - isInvoice: 是否开票 0->否 1->是
    - isPrivacy: 是否开启隐私保护 0->否 1->是
    - isPromotion: 是否活动 0->否 1->是
    - isReply: 是否回复 0->未回复 1->已回复
    - isUpgrade: 是否升级单
    - loginSource: 登录渠道 health->上海健康 ev->企业微信 skin -> 精准护肤
    - orderMonth: 业绩月份yyyyMM
    - orderNo: 订单编号
    - orderStatus: 订单状态 -5->待收礼 -4->活动押货待支付 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - orderStatusList: 订单状态 -5->待收礼 -4->活动押货待支付 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - orderTypes: 订单类型，多个用英文逗号分隔 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 9->签约购转分订单 10->配件订单 11->体验中心自提订单 12->礼物订单 13->微信小店转分订单
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 每页显示数
    - productOrderTypes: 订货类型，多个用英文逗号分隔 1->产品订货 2->资料订货 3->订制品订货
    - productTypes: 商品类型，多个用英文逗号分隔 1->普通商品 2->定制商品 3->组合商品
    - receiverPhone: 收货人手机号
    - serialNo: 产品编码
    - sources: 来源，多个用英文逗号分隔 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0 6->运营后台
    - stockTypes: 库存类型，多个用英文逗号分隔 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    - storeCancel: 是否结点变更  0->否 1->是
    - storeCode: 服务中心编号
    """

    url = "/mgmt/order/orderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
