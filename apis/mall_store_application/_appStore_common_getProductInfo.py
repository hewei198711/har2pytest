import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getProductInfo(params=params, headers=headers):
    """
    获取商品信息
    /appStore/common/getProductInfo

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/common/getProductInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
