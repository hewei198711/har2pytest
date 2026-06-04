import os

from util.client import client

params = {
    "provinceCode": "",  # provinceCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_product_StoreCode(params=params, headers=headers):
    """
    生成服务中心code
    /mgmt/store/product/StoreCode

    参数说明:
    - provinceCode: provinceCode
    """

    url = "/mgmt/store/product/StoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
