import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_queryQrCodeHiddenSetting(headers=headers):
    """
    获取店铺活码隐藏配置
    /appStore/store/queryQrCodeHiddenSetting
    """

    url = "/appStore/store/queryQrCodeHiddenSetting"
    with client.get(url=url, headers=headers) as r:
        return r
