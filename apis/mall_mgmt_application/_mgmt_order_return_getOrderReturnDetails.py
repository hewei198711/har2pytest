import os

from util.client import client

params = {
    "returnNo": "",  # returnNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_getOrderReturnDetails(params=params, headers=headers):
    """
    退货详情
    /mgmt/order/return/getOrderReturnDetails

    参数说明:
    - returnNo: returnNo
    """

    url = "/mgmt/order/return/getOrderReturnDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
