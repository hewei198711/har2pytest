import os

from util.client import client

params = {
    "applyEndTime": "",  # 申请开票结束时间
    "applyStartTime": "",  # 申请开票开始时间
    "balancePayEndTime": "",  # 尾款支付结束时间
    "balancePayStartTime": "",  # 尾款支付开始时间
    "businessMode": 0,  # 经营模式 1->1:3押货 2->85折押货
    "commitEndTime": "",  # 开单结束时间
    "commitStartTime": "",  # 开单开始时间
    "commitTimeOrder": "",  # 下单时间排序字段，asc/desc
    "companyCode": "",  # 分公司编号
    "companyCodeList": [],  # 分公司编号
    "companyName": "",  # 分公司名称
    "companyPermission": 0,  # 账户分公司权限 1->业务,2->财务,3->全选
    "completeTimeOrder": "",  # 完成时间排序字段，asc/desc
    "condition": "",  # 搜索条件
    "creatorCard": "",  # 开单人卡号
    "creatorId": "",  # 开单人id
    "currentCard": "",  # 当前用户卡号
    "currentCompanies": [],  # 当前用户公司
    "currentMemberId": 0,  # 当前用户ID
    "currentMonth": "",  # 当前月份yyyyMM
    "currentStore": "",  # 当前服务中心
    "customerCard": "",  # 顾客会员卡
    "customerCardList": [],  # 顾客卡号
    "customerId": "",  # 顾客id
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerPhoneLike": "",  # 顾客手机号（支持后四位查询）
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    "customerTypeList": [],  # 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    "deliveryCode": "",  # 快递单号
    "depositNo": "",  # 定金单号
    "depositPayEndTime": "",  # 定金支付结束时间
    "depositPayStartTime": "",  # 定金支付开始时间
    "discountLevelList": [],  # 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    "evaluate": 0,  # 评价 0->未评价 1->不满意 2-> 满意 3->非常满意 4->一般
    "evaluateList": [],  # 评价 0->未评价 1->不满意 2-> 满意 3->非常满意 4->一般
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "financeCompanyCode": "",  # 财务分公司编号
    "financeCompanyCodeList": [],  # 财务分公司编号
    "financeCompanyName": "",  # 财务分公司名称
    "from": 0,  # TODO: 添加参数说明
    "isDeliver": 0,  # 订单是否需要发货 0->不发货 1->发货
    "isDisSelfStoreOrder": 0,  # 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    "isInvoice": 0,  # 是否开票 0->否 1->是
    "isOld": 0,  # 是否旧版产品 0->否 1->是
    "isPrivacy": 0,  # 是否开启隐私保护 0->否 1->是
    "isPromotion": 0,  # 是否活动 0->否 1->是
    "isReply": 0,  # 是否回复 0->未回复 1->已回复
    "isSignOrder": False,  # 是否签约单
    "isUpgrade": 0,  # 是否升级单
    "loginSource": "",  # 登录渠道 health->上海健康 ev->企业微信 skin -> 精准护肤
    "orderId": 0,  # 订单id
    "orderMonth": "",  # 业绩月份yyyyMM
    "orderMonthList": [],  # 业绩月份yyyyMM列表
    "orderNo": "",  # 订单编号
    "orderNoList": [],  # 订单编号
    "orderStatusList": [],  # 订单状态 -5->待收礼 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "orderType": 0,  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 12-礼物订单
    "orderTypeList": [],  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 12-礼物订单
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payTimeOrder": "",  # 付款时间排序字段，asc/desc
    "productOrderType": 0,  # 订货类型 1->产品订货 2->资料订货 3->订制品订货
    "productOrderTypes": [],  # 订货类型 1->产品订货 2->资料订货 3->订制品订货
    "productType": 0,  # 商品类型 1->普通商品 2->定制商品 3->组合商品
    "productTypeName": "",  # 产品类型
    "pvValue": 0,  # pv筛选值
    "queryOrderType": 0,  # 1->常规订单 2->时光荟订单
    "queryType": 0,  # 查询类型(默认为null) null->原有订单(包含85折订单)查询 1->85折转分订单 2->85折转分补报订单 3->85折转分订单+85折转分补报订单
    "receiverPhone": "",  # 收货人手机号
    "reviewStatus": 0,  # 审核状态 1->待审核 2->已通过 3->已驳回
    "serialNo": "",  # 产品编码
    "source": 0,  # 来源 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceList": [],  # 来源 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceType": 0,  # 1(立即购买/快速购货)，2(购物车提交),3(结算前销售调整)
    "stockType": 0,  # 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    "stockTypeList": [],  # 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    "storeCancel": 0,  # 是否结点变更  0->否 1->是
    "storeCode": "",  # 服务中心编号
    "storeCodeList": [],  # 门店编号
    "storeName": "",  # 服务中心名称
    "title": "",  # 产品名称
    "waitReviewOrderNoList": [],  # 待审核订单编号数组
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_exportOrderProductStatistics(params=params, headers=headers):
    """
    各系列产品业绩统计表导出
    /appStore/order/exportOrderProductStatistics

    参数说明:
    - applyEndTime: 申请开票结束时间
    - applyStartTime: 申请开票开始时间
    - balancePayEndTime: 尾款支付结束时间
    - balancePayStartTime: 尾款支付开始时间
    - businessMode: 经营模式 1->1:3押货 2->85折押货
    - commitEndTime: 开单结束时间
    - commitStartTime: 开单开始时间
    - commitTimeOrder: 下单时间排序字段，asc/desc
    - companyCode: 分公司编号
    - companyCodeList: 分公司编号
    - companyName: 分公司名称
    - companyPermission: 账户分公司权限 1->业务,2->财务,3->全选
    - completeTimeOrder: 完成时间排序字段，asc/desc
    - condition: 搜索条件
    - creatorCard: 开单人卡号
    - creatorId: 开单人id
    - currentCard: 当前用户卡号
    - currentCompanies: 当前用户公司
    - currentMemberId: 当前用户ID
    - currentMonth: 当前月份yyyyMM
    - currentStore: 当前服务中心
    - customerCard: 顾客会员卡
    - customerCardList: 顾客卡号
    - customerId: 顾客id
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerPhoneLike: 顾客手机号（支持后四位查询）
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    - customerTypeList: 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    - deliveryCode: 快递单号
    - depositNo: 定金单号
    - depositPayEndTime: 定金支付结束时间
    - depositPayStartTime: 定金支付开始时间
    - discountLevelList: 折扣系数等级，1：D-85%；2：C-75%；3：B-70%；4：A-65%
    - evaluate: 评价 0->未评价 1->不满意 2-> 满意 3->非常满意 4->一般
    - evaluateList: 评价 0->未评价 1->不满意 2-> 满意 3->非常满意 4->一般
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - financeCompanyCode: 财务分公司编号
    - financeCompanyCodeList: 财务分公司编号
    - financeCompanyName: 财务分公司名称
    - isDeliver: 订单是否需要发货 0->不发货 1->发货
    - isDisSelfStoreOrder: 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    - isInvoice: 是否开票 0->否 1->是
    - isOld: 是否旧版产品 0->否 1->是
    - isPrivacy: 是否开启隐私保护 0->否 1->是
    - isPromotion: 是否活动 0->否 1->是
    - isReply: 是否回复 0->未回复 1->已回复
    - isSignOrder: 是否签约单
    - isUpgrade: 是否升级单
    - loginSource: 登录渠道 health->上海健康 ev->企业微信 skin -> 精准护肤
    - orderId: 订单id
    - orderMonth: 业绩月份yyyyMM
    - orderMonthList: 业绩月份yyyyMM列表
    - orderNo: 订单编号
    - orderNoList: 订单编号
    - orderStatusList: 订单状态 -5->待收礼 -3->待支付定金 -2->待提交尾款 -1->待支付尾款 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - orderType: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 12-礼物订单
    - orderTypeList: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单 12-礼物订单
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 每页显示数
    - payTimeOrder: 付款时间排序字段，asc/desc
    - productOrderType: 订货类型 1->产品订货 2->资料订货 3->订制品订货
    - productOrderTypes: 订货类型 1->产品订货 2->资料订货 3->订制品订货
    - productType: 商品类型 1->普通商品 2->定制商品 3->组合商品
    - productTypeName: 产品类型
    - pvValue: pv筛选值
    - queryOrderType: 1->常规订单 2->时光荟订单
    - queryType: 查询类型(默认为null) null->原有订单(包含85折订单)查询 1->85折转分订单 2->85折转分补报订单 3->85折转分订单+85折转分补报订单
    - receiverPhone: 收货人手机号
    - reviewStatus: 审核状态 1->待审核 2->已通过 3->已驳回
    - serialNo: 产品编码
    - source: 来源 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - sourceList: 来源 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - sourceType: 1(立即购买/快速购货)，2(购物车提交),3(结算前销售调整)
    - stockType: 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    - stockTypeList: 库存类型 1->公司库存 2->押货库存 3->单位团购库存 4->展业包库存 5->85折押货库存
    - storeCancel: 是否结点变更  0->否 1->是
    - storeCode: 服务中心编号
    - storeCodeList: 门店编号
    - storeName: 服务中心名称
    - title: 产品名称
    - waitReviewOrderNoList: 待审核订单编号数组
    """

    url = "/appStore/order/exportOrderProductStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
