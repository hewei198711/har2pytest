import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_qrcode_importStoreQrCode(headers=headers):
    """
    导入服务中心活码
    /mgmt/store/qrcode/importStoreQrCode
    """

    url = "/mgmt/store/qrcode/importStoreQrCode"
    with client.post(url=url, headers=headers) as r:
        return r
