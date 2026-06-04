import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_getReturnInvoiceDetails(params=params, headers=headers):
    """
    退票详情
    /mgmt/order/return/getReturnInvoiceDetails

    参数说明:
    - id: id
    """

    url = "/mgmt/order/return/getReturnInvoiceDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
