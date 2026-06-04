import os

from util.client import client

data = {
    "productIds": [],  # 商品id
    "showId": "",  # 前端分类
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_onSaleRelShow(data=data, headers=headers):
    """
    上架商品展示
    /mgmt/product/item/onSaleRelShow

    参数说明:
    - productIds: 商品id
    - showId: 前端分类
    """

    url = "/mgmt/product/item/onSaleRelShow"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
