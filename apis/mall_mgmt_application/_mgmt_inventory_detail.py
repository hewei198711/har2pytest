import os

from util.client import client

params = {
    "monthTime": 0,  # 月份，格式为：yyyyMM
    "outIn": 0,  # 出入库：1入库 2出库
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "source": 0,  # 来源：1押货 2押货退货 3商城订单 4顾客退货 5库存调整 6补单
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_detail(params=params, headers=headers):
    """
    查询库存明细
    /mgmt/inventory/detail

    参数说明:
    - monthTime: 月份，格式为：yyyyMM
    - outIn: 出入库：1入库 2出库
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - source: 来源：1押货 2押货退货 3商城订单 4顾客退货 5库存调整 6补单
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
