import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_serviceCenter_certificate(headers=headers):
    """
    服务中心证件
    /appStore/store/serviceCenter/certificate
    """

    url = "/appStore/store/serviceCenter/certificate"
    with client.get(url=url, headers=headers) as r:
        return r
