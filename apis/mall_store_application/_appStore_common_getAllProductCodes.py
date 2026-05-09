import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getAllProductCodes(params=params, headers=headers):
    """
    获取所有匹配的商品编码列表
    /appStore/common/getAllProductCodes

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/common/getAllProductCodes"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
