import os

from util.client import client

params = {
    "productCode": "",  # 商品编码关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_searchMatchedProductCodes(params=params, headers=headers):
    """
    获取所有匹配的商品编码列表
    /appStore/store/dis/mortgage/common/searchMatchedProductCodes

    参数说明:
    - productCode: 商品编码关键字
    """

    url = "/appStore/store/dis/mortgage/common/searchMatchedProductCodes"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
