import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页显示数
    "paymentCompanyNo": "",  # 付款单位编号
    "serviceCenterNo": "",  # 服务中心/公司编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceSheetInvoiceList(data=data, headers=headers):
    """
    计算表.查询可选发票列表
    /appStore/store/invoice/invoiceSheetInvoiceList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页显示数
    - paymentCompanyNo: 付款单位编号
    - serviceCenterNo: 服务中心/公司编号
    """

    url = "/appStore/store/invoice/invoiceSheetInvoiceList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
