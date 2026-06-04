import os

from util.client import client

data = {
    "extInfo": {},  # TODO: 添加参数说明
    "serialNo": "",  # 商品编码
    "type": 0,  # 查询类型，0-模糊，1-精确；默认模糊
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_searchProductLite(data=data, headers=headers):
    """
    查询商品名称
    /mgmt/product/item/searchProductLite

    参数说明:
    - serialNo: 商品编码
    - type: 查询类型，0-模糊，1-精确；默认模糊
    """

    url = "/mgmt/product/item/searchProductLite"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
