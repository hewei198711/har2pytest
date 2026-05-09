import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getAllMatchProductInfo(params=params, headers=headers):
    """
    获取所有匹配的商品列表
    /appStore/common/getAllMatchProductInfo

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/common/getAllMatchProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
