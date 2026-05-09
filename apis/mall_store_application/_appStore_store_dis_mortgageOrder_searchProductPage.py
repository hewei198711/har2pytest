import os

from util.client import client

params = {
    "keyword": "",  # 关键字
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "showId": 0,  # 商品分类id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_searchProductPage(params=params, headers=headers):
    """
    关键字搜索可押货商品分页
    /appStore/store/dis/mortgageOrder/searchProductPage

    参数说明:
    - keyword: 关键字
    - pageNum: 页数
    - pageSize: 页大小
    - showId: 商品分类id
    """

    url = "/appStore/store/dis/mortgageOrder/searchProductPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
