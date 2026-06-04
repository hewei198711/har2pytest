import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_as_applyAfterSale(params=params, headers=headers):
    """
    申请售后是否支持退货、换货
    /mgmt/order/as/applyAfterSale

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/order/as/applyAfterSale"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
