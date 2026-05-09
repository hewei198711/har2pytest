import os

from util.client import client

data = {
    "id": 0,  # 计算表唯一性id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetQueryInvoiceDetail(data=data, headers=headers):
    """
    计算表.查询计算表发票明细
    /appStore/store/invoice/invoiceSheetQueryInvoiceDetail

    参数说明:
    - id: 计算表唯一性id
    """

    url = "/appStore/store/invoice/invoiceSheetQueryInvoiceDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
