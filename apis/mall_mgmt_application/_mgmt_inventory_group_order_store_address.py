import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_store_address(params=params, headers=headers):
    """
    获取服务中心收货信息
    /mgmt/inventory/group-order/store-address

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/group-order/store-address"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
