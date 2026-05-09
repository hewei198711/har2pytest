import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_selectInvoiceTypeInfo(headers=headers):
    """
    selectInvoiceTypeInfo
    /appStore/store/invoice/selectInvoiceTypeInfo
    """

    url = "/appStore/store/invoice/selectInvoiceTypeInfo"
    with client.get(url=url, headers=headers) as r:
        return r
