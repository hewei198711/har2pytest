import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_orderSign_getPromotionList(params=params, headers=headers):
    """
    签约活动列表-签约购报表筛选条件使用
    /appStore/orderSign/getPromotionList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/appStore/orderSign/getPromotionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
