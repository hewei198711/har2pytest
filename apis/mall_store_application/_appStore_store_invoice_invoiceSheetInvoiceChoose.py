import os

from util.client import client

data = {
    "invoiceIds": "",  # 所选发票记录唯一性id组合，用【,】分隔
    "serviceCenterNo": "",  # 服务中心/公司编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetInvoiceChoose(data=data, headers=headers):
    """
    计算表.选择发票，返回计算表数据
    /appStore/store/invoice/invoiceSheetInvoiceChoose

    参数说明:
    - invoiceIds: 所选发票记录唯一性id组合，用【,】分隔
    - serviceCenterNo: 服务中心/公司编号
    """

    url = "/appStore/store/invoice/invoiceSheetInvoiceChoose"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
