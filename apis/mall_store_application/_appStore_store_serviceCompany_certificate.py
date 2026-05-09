import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_serviceCompany_certificate(headers=headers):
    """
    服务公司证件
    /appStore/store/serviceCompany/certificate
    """

    url = "/appStore/store/serviceCompany/certificate"
    with client.get(url=url, headers=headers) as r:
        return r
