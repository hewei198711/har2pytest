import os

from util.client import client

params = {
    "expressNo": "",  # expressNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_expressProgress(params=params, headers=headers):
    """
    发票签收查询
    /appStore/store/invoice/expressProgress

    参数说明:
    - expressNo: expressNo
    """

    url = "/appStore/store/invoice/expressProgress"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
