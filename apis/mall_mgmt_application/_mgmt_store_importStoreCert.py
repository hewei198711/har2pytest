import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importStoreCert(headers=headers):
    """
    导入电子印章认证信息
    /mgmt/store/importStoreCert
    """

    url = "/mgmt/store/importStoreCert"
    with client.post(url=url, headers=headers) as r:
        return r
