import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetPaymentChoose(headers=headers):
    """
    计算表.选择付款单位
    /appStore/store/invoice/invoiceSheetPaymentChoose
    """

    url = "/appStore/store/invoice/invoiceSheetPaymentChoose"
    with client.get(url=url, headers=headers) as r:
        return r
