import os

from util.client import client

params = {
    "itemCode": "",  # itemCode
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_item_stock(params=params, headers=headers):
    """
    查询商品库存信息
    /mgmt/dis-inventory/item-stock

    参数说明:
    - itemCode: itemCode
    - storeCode: storeCode
    """

    url = "/mgmt/dis-inventory/item-stock"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
