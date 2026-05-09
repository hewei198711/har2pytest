import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_luckyActivity_storeSelectLucky(headers=headers):
    """
    门店查询当前进行中、已结束的抽奖活动下拉列表
    /appStore/luckyActivity/storeSelectLucky
    """

    url = "/appStore/luckyActivity/storeSelectLucky"
    with client.get(url=url, headers=headers) as r:
        return r
