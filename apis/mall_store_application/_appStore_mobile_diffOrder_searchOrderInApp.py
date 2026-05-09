import os

from util.client import client

params = {
    "keyword": "",  # 关键字
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_diffOrder_searchOrderInApp(params=params, headers=headers):
    """
    APP货损货差单分页查询
    /appStore/mobile/diffOrder/searchOrderInApp

    参数说明:
    - keyword: 关键字
    - pageNum: 页数
    - pageSize: 每页大小
    """

    url = "/appStore/mobile/diffOrder/searchOrderInApp"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
