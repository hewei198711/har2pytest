import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 换货凭证URL列表
    "exchangeNo": "",  # 换货单号
    "exchangeType": 0,  # 换货方式 1->先退后换 2->秒换 3->先换后退
    "junkHandleType": 0,  # 旧品处理方式 1->退回中转仓 2->分公司报废
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
    "reason1": "",  # 换货原因
    "reason1Id": 0,  # 换货原因id
    "reason1Remark": "",  # 换货原因备注
    "reason2": "",  # 换货原因2
    "reason2Id": 0,  # 换货原因2id
    "reason2Remark": "",  # 换货原因2备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_updateOrderExchange(data=data, headers=headers):
    """
    修改换货申请
    /mgmt/order/exchange/updateOrderExchange

    参数说明:
    - attachmentUrlList: 换货凭证URL列表
    - exchangeNo: 换货单号
    - exchangeType: 换货方式 1->先退后换 2->秒换 3->先换后退
    - junkHandleType: 旧品处理方式 1->退回中转仓 2->分公司报废
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
    - reason1: 换货原因
    - reason1Id: 换货原因id
    - reason1Remark: 换货原因备注
    - reason2: 换货原因2
    - reason2Id: 换货原因2id
    - reason2Remark: 换货原因2备注
    """

    url = "/mgmt/order/exchange/updateOrderExchange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
