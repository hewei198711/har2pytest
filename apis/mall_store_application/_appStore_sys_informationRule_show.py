import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_informationRule_show(headers=headers):
    """
    法规咨询-展示
    /appStore/sys/informationRule/show
    """

    url = "/appStore/sys/informationRule/show"
    with client.get(url=url, headers=headers) as r:
        return r
