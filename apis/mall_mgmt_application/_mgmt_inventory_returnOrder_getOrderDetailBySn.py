import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_getOrderDetailBySn(params=params, headers=headers):
    """
    后台通过sn查询押货退货单详情
    /mgmt/inventory/returnOrder/getOrderDetailBySn

    参数说明:
    - orderSn: orderSn
    """

    url = "/mgmt/inventory/returnOrder/getOrderDetailBySn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
