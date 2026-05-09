import os

from util.client import client

data = {
    "invoiceType": 0,  # 发票类型，1：增值税普通发票； 2：增值税电子普通发票；3：增值税普通发票（卷式）；4：通用机打发票；5：通用机打（电子）发票；6：通用手工发票；7：通用定额发票；8：增值税专用发票；9：增值税电子专用发票；10：全电普票
    "invoiceUrl": "",  # 发票Url
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_invoiceBduOcrScan(data=data, headers=headers):
    """
    百度OCR发票识别
    /appStore/store/invoice/invoiceBduOcrScan

    参数说明:
    - invoiceType: 发票类型，1：增值税普通发票； 2：增值税电子普通发票；3：增值税普通发票（卷式）；4：通用机打发票；5：通用机打（电子）发票；6：通用手工发票；7：通用定额发票；8：增值税专用发票；9：增值税电子专用发票；10：全电普票
    - invoiceUrl: 发票Url
    """

    url = "/appStore/store/invoice/invoiceBduOcrScan"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
