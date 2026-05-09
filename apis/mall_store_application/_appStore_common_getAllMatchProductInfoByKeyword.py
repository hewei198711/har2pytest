import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getAllMatchProductInfoByKeyword(params=params, headers=headers):
    """
    关键字获取所有匹配的商品列表
    /appStore/common/getAllMatchProductInfoByKeyword

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/common/getAllMatchProductInfoByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
