import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_fetchPostSaleProductPairsByKeyword(params=params, headers=headers):
    """
    关键字获取所有匹配的商品列表(押货售后)
    /appStore/store/dis/mortgage/common/fetchPostSaleProductPairsByKeyword

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/store/dis/mortgage/common/fetchPostSaleProductPairsByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
