import os

from util.client import client

params = {
    "month": 0,  # 月结月份
    "orderNo": "",  # 团购单号
    "productCode": "",  # 产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_stock_detail(params=params, headers=headers):
    """
    获取团购单库存明细
    /mgmt/inventory/group-order/stock/detail

    参数说明:
    - month: 月结月份
    - orderNo: 团购单号
    - productCode: 产品编号
    """

    url = "/mgmt/inventory/group-order/stock/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
