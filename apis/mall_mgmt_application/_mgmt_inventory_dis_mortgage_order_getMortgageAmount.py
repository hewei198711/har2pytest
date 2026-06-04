import os

from util.client import client

params = {
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_getMortgageAmount(params=params, headers=headers):
    """
    查询店铺押货余额与限额
    /mgmt/inventory/dis/mortgage/order/getMortgageAmount

    参数说明:
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/dis/mortgage/order/getMortgageAmount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
