import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_home_statistic(headers=headers):
    """
    统计数据
    /appStore/mobile/home/statistic
    """

    url = "/appStore/mobile/home/statistic"
    with client.get(url=url, headers=headers) as r:
        return r
