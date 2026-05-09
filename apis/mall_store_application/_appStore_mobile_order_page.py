import os

from util.client import client

params = {
    "isDisSelfStoreOrder": 0,  # 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    "keyword": "",  # 关键字搜索，退货单号/购货人会员卡号/购货人姓名/产品名称
    "orderStatus": 0,  # 订单状态 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "orderType": 0,  # 订单类型 1-正常订单 2->补报订单 5->85折转分订单(店交付订单) 6->85折转分补报订单(店交付补报订单) 8->签约购订单 9->签约购转分订单
    "orderWay": 0,  # 下单方式 1->自购订单 2->代购订单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_order_page(params=params, headers=headers):
    """
    订单分页查询
    /appStore/mobile/order/page

    参数说明:
    - isDisSelfStoreOrder: 是否是85折会员、VIP自购选择服务中心自提订单 0->否 1->是
    - keyword: 关键字搜索，退货单号/购货人会员卡号/购货人姓名/产品名称
    - orderStatus: 订单状态 0->待审核 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - orderType: 订单类型 1-正常订单 2->补报订单 5->85折转分订单(店交付订单) 6->85折转分补报订单(店交付补报订单) 8->签约购订单 9->签约购转分订单
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/mobile/order/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
