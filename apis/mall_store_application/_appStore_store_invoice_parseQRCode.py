import os

from util.client import client

data = {
    "qrCode": "",  # 解析二维码参数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_invoice_parseQRCode(data=data, headers=headers):
    """
    解析发票二维码
    /appStore/store/invoice/parseQRCode

    参数说明:
    - qrCode: 解析二维码参数
    """

    url = "/appStore/store/invoice/parseQRCode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
