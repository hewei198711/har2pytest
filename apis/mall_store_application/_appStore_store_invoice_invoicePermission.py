import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoicePermission(headers=headers):
    """
    是否有发票采集，发票进度权限，1：有权限，0：无权限
    /appStore/store/invoice/invoicePermission
    """

    url = "/appStore/store/invoice/invoicePermission"
    with client.get(url=url, headers=headers) as r:
        return r
