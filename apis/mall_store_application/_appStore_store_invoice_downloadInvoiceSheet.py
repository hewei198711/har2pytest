import os

from util.client import client

params = {
    "sheetId": 0,  # sheetId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_downloadInvoiceSheet(params=params, headers=headers):
    """
    下载计算表
    /appStore/store/invoice/downloadInvoiceSheet

    参数说明:
    - sheetId: sheetId
    """

    url = "/appStore/store/invoice/downloadInvoiceSheet"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
