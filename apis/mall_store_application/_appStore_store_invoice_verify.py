import os

from util.client import client

data = {
    "amount": 0.0,  # 发票金额
    "checkCode": "",  # 校验码（后6位）
    "id": 0,  # 发票主键Id，新增不传，修改时必传
    "invoiceCode": "",  # 发票代码
    "invoiceDate": "",  # 开票日期
    "invoiceNumber": "",  # 发票号码起
    "invoiceNumberEnd": "",  # 发票号码止
    "invoiceType": 0,  # 发票类型，1：增值税普通发票； 2：增值税电子普通发票；3：增值税普通发票（卷式）；4：通用机打发票；5：通用机打（电子）发票；6：通用手工发票；7：通用定额发票；8：增值税专用发票；9：增值税电子专用发票；10：全电普票
    "taxFreeAmount": 0.0,  # 不含税金额
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_verify(data=data, headers=headers):
    """
    发票查验，验证真伪，是否重复
    /appStore/store/invoice/verify

    参数说明:
    - amount: 发票金额
    - checkCode: 校验码（后6位）
    - id: 发票主键Id，新增不传，修改时必传
    - invoiceCode: 发票代码
    - invoiceDate: 开票日期
    - invoiceNumber: 发票号码起
    - invoiceNumberEnd: 发票号码止
    - invoiceType: 发票类型，1：增值税普通发票； 2：增值税电子普通发票；3：增值税普通发票（卷式）；4：通用机打发票；5：通用机打（电子）发票；6：通用手工发票；7：通用定额发票；8：增值税专用发票；9：增值税电子专用发票；10：全电普票
    - taxFreeAmount: 不含税金额
    """

    url = "/appStore/store/invoice/verify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
