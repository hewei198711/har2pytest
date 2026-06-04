import os

from util.client import client

params = {
    "applySource": 0,  # 申请来源 1->顾客申请 2->公司申请
    "applyTimeBegin": "",  # 申请开始时间 #格式yyyy-MM-dd
    "applyTimeEnd": "",  # 申请结束时间 #格式yyyy-MM-dd
    "companyCode": "",  # 分公司编号
    "companyName": "",  # 分公司名称
    "creatorCard": "",  # 开单人卡号
    "creatorId": 0,  # 开单人id
    "customerCard": "",  # 顾客卡号
    "customerId": 0,  # 顾客id
    "exchangeNo": "",  # 换货单号
    "exchangeStatus": 0,  # 换货单状态  1->待审核 2->待退回 3->待验货 4->待回寄 5->待确认 98->已取消  99->已完成
    "exchangeType": 0,  # 换货方式 1->先退后换 2->秒换 3->先换后退
    "expressType": 0,  # 配送方式 1->服务中心自提 2->公司配送
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "pushStatus": 0,  # 推送状态 0->未推送 1->已推送
    "returnExpressType": 0,  # 退回方式  1->物流发货 2->顾客自带 3->上门取件
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "userCard": "",  # 用户卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_countOrderExchangeList(params=params, headers=headers):
    """
    订单换货列表统计
    /mgmt/order/exchange/countOrderExchangeList

    参数说明:
    - applySource: 申请来源 1->顾客申请 2->公司申请
    - applyTimeBegin: 申请开始时间 #格式yyyy-MM-dd
    - applyTimeEnd: 申请结束时间 #格式yyyy-MM-dd
    - companyCode: 分公司编号
    - companyName: 分公司名称
    - creatorCard: 开单人卡号
    - creatorId: 开单人id
    - customerCard: 顾客卡号
    - customerId: 顾客id
    - exchangeNo: 换货单号
    - exchangeStatus: 换货单状态  1->待审核 2->待退回 3->待验货 4->待回寄 5->待确认 98->已取消  99->已完成
    - exchangeType: 换货方式 1->先退后换 2->秒换 3->先换后退
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - pushStatus: 推送状态 0->未推送 1->已推送
    - returnExpressType: 退回方式  1->物流发货 2->顾客自带 3->上门取件
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - userCard: 用户卡号
    """

    url = "/mgmt/order/exchange/countOrderExchangeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
