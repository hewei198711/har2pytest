import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_productData_getProductInfoByProductCode(params=params, headers=headers):
    """
    获取产品信息
    /mgmt/dataAdmin/productData/getProductInfoByProductCode

    参数说明:
    - productCode: productCode
    """

    url = "/mgmt/dataAdmin/productData/getProductInfoByProductCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
