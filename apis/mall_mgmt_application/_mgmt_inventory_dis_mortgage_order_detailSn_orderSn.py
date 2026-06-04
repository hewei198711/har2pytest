import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_detailSn_orderSn(params=params, headers=headers):
    """
    押货单详情(编号查询)
    /mgmt/inventory/dis/mortgage/order/detailSn/{orderSn}

    参数说明:
    - orderSn: orderSn
    """

    url = f"/mgmt/inventory/dis/mortgage/order/detailSn/{params['orderSn']}"
    with client.get(url=url, headers=headers) as r:
        return r
