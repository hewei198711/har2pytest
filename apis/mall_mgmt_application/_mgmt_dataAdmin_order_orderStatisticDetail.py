import os

from util.client import client

params = {
    "busiType": 0,  # 业务类型:0-码上有名
    "endCreateTime": "",  # 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "endOrderMonth": "",  # 结束业绩月份yyyyMM 202104
    "orderRoute": "",  # 订单来源：0. 立即购买；1. 快速购货；2.购物车提交；3. 结算前销售调整；4. 定制商品购买；5. 辅销品购买；6. 旧版商品购买；7. 调差购买；8. 85折转分订单；9. 85折转分补报订单；10.单位团购报单;11-签约购;12-H5代客选品;13-码上有名
    "orderRouteList": [],  # TODO: 添加参数说明
    "serialNo": "",  # 产品编码
    "source": "",  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceList": [],  # TODO: 添加参数说明
    "startCreateTime": "",  # 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "startOrderMonth": "",  # 开始业绩月份yyyyMM 202104
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_order_orderStatisticDetail(params=params, headers=headers):
    """
    订单统计明細
    /mgmt/dataAdmin/order/orderStatisticDetail

    参数说明:
    - busiType: 业务类型:0-码上有名
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - endOrderMonth: 结束业绩月份yyyyMM 202104
    - orderRoute: 订单来源：0. 立即购买；1. 快速购货；2.购物车提交；3. 结算前销售调整；4. 定制商品购买；5. 辅销品购买；6. 旧版商品购买；7. 调差购买；8. 85折转分订单；9. 85折转分补报订单；10.单位团购报单;11-签约购;12-H5代客选品;13-码上有名
    - serialNo: 产品编码
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startOrderMonth: 开始业绩月份yyyyMM 202104
    """

    url = "/mgmt/dataAdmin/order/orderStatisticDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
