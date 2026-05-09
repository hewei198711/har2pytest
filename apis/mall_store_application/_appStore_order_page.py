import os

from util.client import client

params = {
    "commitEndTime": "",  # 开单结束时间
    "commitStartTime": "",  # 开单开始时间
    "commitTimeOrder": "",  # 下单时间排序字段，asc/desc
    "completeTimeOrder": "",  # 完成时间排序字段，asc/desc
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客会员卡
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerPhoneLike": "",  # 顾客手机号（支持后四位查询）
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    "deliveryCode": "",  # 快递单号
    "isDisSelfStoreOrder": 0,  # 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    "orderNo": "",  # 订单编号
    "orderNoList": [],  # 订单编号
    "orderStatusList": [],  # 订单状态 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "orderType": 0,  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单
    "orderTypeList": [],  # 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "payTimeOrder": "",  # 付款时间排序字段，asc/desc
    "product": "",  # 产品编码/名称
    "productOrderTypes": [],  # 订货类型 1->产品订货 2->资料订货 3->订制品订货
    "source": 0,  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_page(params=params, headers=headers):
    """
    订单列表（分页）
    /appStore/order/page

    参数说明:
    - commitEndTime: 开单结束时间
    - commitStartTime: 开单开始时间
    - commitTimeOrder: 下单时间排序字段，asc/desc
    - completeTimeOrder: 完成时间排序字段，asc/desc
    - creatorCard: 开单人卡号
    - customerCard: 顾客会员卡
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerPhoneLike: 顾客手机号（支持后四位查询）
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->微店 4->云商
    - deliveryCode: 快递单号
    - isDisSelfStoreOrder: 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    - orderNo: 订单编号
    - orderNoList: 订单编号
    - orderStatusList: 订单状态 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - orderType: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单
    - orderTypeList: 订单类型 1-正常订单 2->补报订单 3->调差订单 4->单位团购转分订单 5->85折转分订单 6->85折转分补报订单 7->预售订单 8->签约购订单
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 页大小
    - payTimeOrder: 付款时间排序字段，asc/desc
    - product: 产品编码/名称
    - productOrderTypes: 订货类型 1->产品订货 2->资料订货 3->订制品订货
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    """

    url = "/appStore/order/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
