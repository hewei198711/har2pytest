import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_complex_recommendList(params=params, headers=headers):
    """
    获取推荐组合列表
    /appStore/complex/recommendList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - promotionId: promotionId
    """

    url = "/appStore/complex/recommendList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
