import os

from util.client import client

data = {
    "list": [{"mortgagePrice": 0.0, "productCode": ""}],  # 商品列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_checkSecurityPrice(data=data, headers=headers):
    """
    查询商品价格是否发生变动
    /mgmt/inventory/order/checkSecurityPrice

    参数说明:
    - list: 商品列表
    - list.mortgagePrice: 押货价
    - list.productCode: 商品编码
    """

    url = "/mgmt/inventory/order/checkSecurityPrice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
