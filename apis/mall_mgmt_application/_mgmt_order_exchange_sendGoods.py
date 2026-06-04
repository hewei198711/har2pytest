import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 回寄凭证URL列表
    "sendExpressName": "",  # 快递公司名称
    "sendExpressNo": "",  # 快递运单号
    "sendExpressType": 0,  # 回寄方式  1->物流配送 2->顾客自提
    "serviceNo": "",  # 售后单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_sendGoods(data=data, headers=headers):
    """
    货品回寄
    /mgmt/order/exchange/sendGoods

    参数说明:
    - attachmentUrlList: 回寄凭证URL列表
    - sendExpressName: 快递公司名称
    - sendExpressNo: 快递运单号
    - sendExpressType: 回寄方式  1->物流配送 2->顾客自提
    - serviceNo: 售后单号
    """

    url = "/mgmt/order/exchange/sendGoods"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
