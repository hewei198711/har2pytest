import os

from util.client import client

data = {
    "productDtoList": [{"productCode": "", "productNum": 0}],  # 需要修改的商品
    "storeCode": "",  # 店铺中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_checkProductDistribution(data=data, headers=headers):
    """
    分配量校验接口
    /mgmt/inventory/order/checkProductDistribution

    参数说明:
    - productDtoList: 需要修改的商品
    - productDtoList.productCode: 商品编码
    - productDtoList.productNum: 商品数量
    - storeCode: 店铺中心编号
    """

    url = "/mgmt/inventory/order/checkProductDistribution"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
