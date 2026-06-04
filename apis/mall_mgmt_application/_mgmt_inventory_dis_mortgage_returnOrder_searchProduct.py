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


def _mgmt_inventory_dis_mortgage_returnOrder_searchProduct(params=params, headers=headers):
    """
    商品编码搜索退货商品信息
    /mgmt/inventory/dis/mortgage/returnOrder/searchProduct

    参数说明:
    - productCode: 商品编码
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/searchProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
