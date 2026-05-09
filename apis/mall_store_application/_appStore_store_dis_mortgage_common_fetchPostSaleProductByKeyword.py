import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_fetchPostSaleProductByKeyword(params=params, headers=headers):
    """
    关键字搜索商品及库存(押货售后)
    /appStore/store/dis/mortgage/common/fetchPostSaleProductByKeyword

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/store/dis/mortgage/common/fetchPostSaleProductByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
