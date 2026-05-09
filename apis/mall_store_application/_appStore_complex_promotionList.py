import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_promotionList(params=params, headers=headers):
    """
    获取签约购活动列表
    /appStore/complex/promotionList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/appStore/complex/promotionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
