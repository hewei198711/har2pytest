import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetToSign(params=params, headers=headers):
    """
    计算表.去签署
    /appStore/store/invoice/invoiceSheetToSign

    参数说明:
    - id: id
    """

    url = "/appStore/store/invoice/invoiceSheetToSign"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
