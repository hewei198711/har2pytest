import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_intro(headers=headers):
    """
    获取签约购活动介绍4.0
    /appStore/complex/intro
    """

    url = "/appStore/complex/intro"
    with client.get(url=url, headers=headers) as r:
        return r
