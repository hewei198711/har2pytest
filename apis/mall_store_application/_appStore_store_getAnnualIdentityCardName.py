import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getAnnualIdentityCardName(headers=headers):
    """
    获取身份证年审姓名信息
    /appStore/store/getAnnualIdentityCardName
    """

    url = "/appStore/store/getAnnualIdentityCardName"
    with client.get(url=url, headers=headers) as r:
        return r
