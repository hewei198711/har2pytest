import os

from util.client import client

params = {
    "sheetId": 0,  # sheetId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_downloadInvoiceSheet(params=params, headers=headers):
    """
    下载计算表
    /mgmt/fin/wallet/downloadInvoiceSheet

    参数说明:
    - sheetId: sheetId
    """

    url = "/mgmt/fin/wallet/downloadInvoiceSheet"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
