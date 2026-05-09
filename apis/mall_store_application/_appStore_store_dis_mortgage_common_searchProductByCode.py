import os

from util.client import client

params = {
    "productCode": "",  # 商品编码
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_searchProductByCode(params=params, headers=headers):
    """
    按商品编码精确查询商品
    /appStore/store/dis/mortgage/common/searchProductByCode

    参数说明:
    - productCode: 商品编码
    - storeCode: 店铺编号
    """

    url = "/appStore/store/dis/mortgage/common/searchProductByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
