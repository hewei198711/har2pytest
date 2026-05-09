import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_serviceCompany_list(headers=headers):
    """
    服务公司列表
    /appStore/store/serviceCompany/list
    """

    url = "/appStore/store/serviceCompany/list"
    with client.get(url=url, headers=headers) as r:
        return r
