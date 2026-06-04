import os

from util.client import client

params = {
    "orderNo": "",  # 团购单编号
    "productCode": "",  # 商品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_stock_adjust_audit_list(params=params, headers=headers):
    """
    调整团购单库存审核列表查询
    /mgmt/inventory/group-order/stock/adjust/audit/list

    参数说明:
    - orderNo: 团购单编号
    - productCode: 商品编号
    """

    url = "/mgmt/inventory/group-order/stock/adjust/audit/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
