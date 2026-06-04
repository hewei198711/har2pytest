import os

from util.client import client

params = {
    "from": 0,  # TODO: 添加参数说明
    "isDifference": 0,  # 交付差额是否为负 0->否 1->是
    "orderMonth": "",  # 业绩月份
    "orderNo": "",  # 订单号
    "orderType": 0,  # 订单类型 1->商城报单 2->商城退单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "storeCode": "",  # 服务中心编号
    "tradingEndTime": "",  # 交易结束时间
    "tradingStartTime": "",  # 交易开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getOrderSettlementDetail(params=params, headers=headers):
    """
    交付结算详情
    /mgmt/order/getOrderSettlementDetail

    参数说明:
    - isDifference: 交付差额是否为负 0->否 1->是
    - orderMonth: 业绩月份
    - orderNo: 订单号
    - orderType: 订单类型 1->商城报单 2->商城退单
    - pageNum: 页数
    - pageSize: 每页显示数
    - storeCode: 服务中心编号
    - tradingEndTime: 交易结束时间
    - tradingStartTime: 交易开始时间
    """

    url = "/mgmt/order/getOrderSettlementDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
