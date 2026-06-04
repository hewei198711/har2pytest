import os

from util.client import client

data = {
    "adjustNum": 0,  # 调整数量 负->减少, 正->增加
    "orderNo": "",  # 团购单编号
    "productCode": "",  # 商品编号
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_stock_adjust_audit_add(data=data, headers=headers):
    """
    添加调整团购单库存审核
    /mgmt/inventory/group-order/stock/adjust/audit/add

    参数说明:
    - adjustNum: 调整数量 负->减少, 正->增加
    - orderNo: 团购单编号
    - productCode: 商品编号
    - remark: 备注
    """

    url = "/mgmt/inventory/group-order/stock/adjust/audit/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
