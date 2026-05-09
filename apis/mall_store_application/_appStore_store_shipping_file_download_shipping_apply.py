import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_shipping_file_download_shipping_apply(headers=headers):
    """
    申请模板下载
    /appStore/store/shipping/file/download-shipping-apply
    """

    url = "/appStore/store/shipping/file/download-shipping-apply"
    with client.get(url=url, headers=headers) as r:
        return r
