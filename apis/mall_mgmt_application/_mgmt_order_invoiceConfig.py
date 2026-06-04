import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_invoiceConfig(headers=headers):
    """
    查询订单发票配置信息
    /mgmt/order/invoiceConfig
    """

    url = "/mgmt/order/invoiceConfig"
    with client.get(url=url, headers=headers) as r:
        return r
