import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_informationRule_isShow(headers=headers):
    """
    法规咨询-是否展示
    /appStore/sys/informationRule/isShow
    """

    url = "/appStore/sys/informationRule/isShow"
    with client.get(url=url, headers=headers) as r:
        return r
