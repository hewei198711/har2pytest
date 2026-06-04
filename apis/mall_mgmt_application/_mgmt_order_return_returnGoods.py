import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 退回凭证URL列表
    "expectedTime": "",  # 期望上门时间 yyyy-MM-dd HH:mm
    "paymentType": 0,  # 付款方式 1->顾客自费 2-> 完美支付
    "returnContactNumber": "",  # 退回联系电话
    "returnExpressName": "",  # 快递公司名称
    "returnExpressNo": "",  # 快递运单号
    "returnExpressType": 0,  # 退回方式  1->邮寄 2->自带 3-> 上门取件
    "returnFreight": 0.0,  # 用户退回商品运费
    "senderAddress": "",  # 寄件人地址
    "senderName": "",  # 寄件人姓名
    "senderPhone": "",  # 寄件人姓名
    "serviceNo": "",  # 售后单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_returnGoods(data=data, headers=headers):
    """
    货品退回
    /mgmt/order/return/returnGoods

    参数说明:
    - attachmentUrlList: 退回凭证URL列表
    - expectedTime: 期望上门时间 yyyy-MM-dd HH:mm
    - paymentType: 付款方式 1->顾客自费 2-> 完美支付
    - returnContactNumber: 退回联系电话
    - returnExpressName: 快递公司名称
    - returnExpressNo: 快递运单号
    - returnExpressType: 退回方式  1->邮寄 2->自带 3-> 上门取件
    - returnFreight: 用户退回商品运费
    - senderAddress: 寄件人地址
    - senderName: 寄件人姓名
    - senderPhone: 寄件人姓名
    - serviceNo: 售后单号
    """

    url = "/mgmt/order/return/returnGoods"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
