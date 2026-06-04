import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_calcRefundAmount(params=params, headers=headers):
    """
    计算订单退款金额
    /mgmt/order/return/calcRefundAmount

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/order/return/calcRefundAmount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
