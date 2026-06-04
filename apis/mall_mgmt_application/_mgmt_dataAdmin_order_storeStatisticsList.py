import os

from util.client import client

params = {
    "adminType": 0,  # 管理员身份类型：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "busiType": 0,  # 业务类型:0-码上有名
    "endCreateTime": "",  # 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "endOrderMonth": "",  # 结束业绩月份yyyyMM 202104
    "orderRoute": "",  # 订单来源：0. 立即购买；1. 快速购货；2.购物车提交；3. 结算前销售调整；4. 定制商品购买；5. 辅销品购买；6. 旧版商品购买；7. 调差购买；8. 85折转分订单；9. 85折转分补报订单；10.单位团购报单;11-签约购;12-H5代客选品;13-码上有名
    "orderRouteList": [],  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "serialNo": "",  # 产品编码
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型:0-下单订单数,1-支付订单数,2-退货订单数,3-取消订单数,4-下单订单金额,5-支付订单金额,6-退货订单金额
    "source": "",  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "sourceList": [],  # TODO: 添加参数说明
    "startCreateTime": "",  # 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "startOrderMonth": "",  # 开始业绩月份yyyyMM 202104
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_order_storeStatisticsList(params=params, headers=headers):
    """
    查询交付门店统计明细
    /mgmt/dataAdmin/order/storeStatisticsList

    参数说明:
    - adminType: 管理员身份类型：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - busiType: 业务类型:0-码上有名
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - endOrderMonth: 结束业绩月份yyyyMM 202104
    - orderRoute: 订单来源：0. 立即购买；1. 快速购货；2.购物车提交；3. 结算前销售调整；4. 定制商品购买；5. 辅销品购买；6. 旧版商品购买；7. 调差购买；8. 85折转分订单；9. 85折转分补报订单；10.单位团购报单;11-签约购;12-H5代客选品;13-码上有名
    - serialNo: 产品编码
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型:0-下单订单数,1-支付订单数,2-退货订单数,3-取消订单数,4-下单订单金额,5-支付订单金额,6-退货订单金额
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startOrderMonth: 开始业绩月份yyyyMM 202104
    """

    url = "/mgmt/dataAdmin/order/storeStatisticsList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
