import os

from util.client import client

data = {
    "docType": 0,  # 单据类型：1=购货单 2=发货单
    "orderNo": "",  # 订单编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderPrintRecord(data=data, headers=headers):
    """
    订单打印记录
    /mgmt/order/orderPrintRecord

    参数说明:
    - docType: 单据类型：1=购货单 2=发货单
    - orderNo: 订单编号
    """

    url = "/mgmt/order/orderPrintRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
