import os

from util.client import client

data = {
    "applySource": 0,  # 来源 0->总公司代客申请 1->顾客申请 2->公司申请
    "attachmentUrlList": [],  # 换货凭证URL列表
    "exchangeType": 0,  # 换货方式 1->先退后换 2->秒换 3->先换后退
    "junkHandleType": 0,  # 旧品处理方式 1->分公司处理 2->中转仓处理
    "orderExchangeProducts": [
        {
            "batchNumber": "",
            "endData": "",
            "expiryData": "",
            "firstUseTime": "",
            "problemDesc": "",
            "problemStatus": 0,
            "productCode": "",
            "productName": "",
            "qrCode": "",
            "quantity": 0,
            "usePeriod": 0,
        }
    ],  # 换货商品列表
    "orderNo": "",  # 订单编号
    "reason1": "",  # 换货一级原因
    "reason1Id": 0,  # 换货一级原因id
    "reason1Remark": "",  # 换货一级原因备注
    "reason2": "",  # 换货二级原因
    "reason2Id": 0,  # 换货二级原因id
    "reason2Remark": "",  # 换货二级原因备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_applyExchange(data=data, headers=headers):
    """
    申请换货
    /mgmt/order/exchange/applyExchange

    参数说明:
    - applySource: 来源 0->总公司代客申请 1->顾客申请 2->公司申请
    - attachmentUrlList: 换货凭证URL列表
    - exchangeType: 换货方式 1->先退后换 2->秒换 3->先换后退
    - junkHandleType: 旧品处理方式 1->分公司处理 2->中转仓处理
    - orderExchangeProducts: 换货商品列表
    - orderExchangeProducts.batchNumber: 批号
    - orderExchangeProducts.endData: 限用日期
    - orderExchangeProducts.expiryData: 生产日期/有效期
    - orderExchangeProducts.firstUseTime: 初次使用时间
    - orderExchangeProducts.problemDesc: 详细问题描述(产品内容物状态)
    - orderExchangeProducts.problemStatus: 问题发生状态 1->初次开封使用发现 2->使用过程中发现
    - orderExchangeProducts.productCode: 商品编码
    - orderExchangeProducts.productName: 商品名称
    - orderExchangeProducts.qrCode: 二维码
    - orderExchangeProducts.quantity: 售后数量
    - orderExchangeProducts.usePeriod: 日常使用时段 1->早 2-中 3->晚
    - orderNo: 订单编号
    - reason1: 换货一级原因
    - reason1Id: 换货一级原因id
    - reason1Remark: 换货一级原因备注
    - reason2: 换货二级原因
    - reason2Id: 换货二级原因id
    - reason2Remark: 换货二级原因备注
    """

    url = "/mgmt/order/exchange/applyExchange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
