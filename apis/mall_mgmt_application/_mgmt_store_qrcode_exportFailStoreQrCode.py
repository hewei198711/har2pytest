import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_exportFailStoreQrCode(headers=headers):
    """
    导出服务中心活码失败列表
    /mgmt/store/qrcode/exportFailStoreQrCode
    """

    url = "/mgmt/store/qrcode/exportFailStoreQrCode"
    with client.get(url=url, headers=headers) as r:
        return r
