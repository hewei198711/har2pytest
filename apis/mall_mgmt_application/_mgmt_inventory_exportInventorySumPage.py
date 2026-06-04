import os

from util.client import client

params = {
    "catalogId": 0,  # 产品类型id
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "stock": 0,  # 库存数量
    "stockOperation": 0,  # 库存查询操作: 1:>= 2:> 3:<= 4:<
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_exportInventorySumPage(params=params, headers=headers):
    """
    导出库存汇总分页
    /mgmt/inventory/exportInventorySumPage

    参数说明:
    - catalogId: 产品类型id
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - stock: 库存数量
    - stockOperation: 库存查询操作: 1:>= 2:> 3:<= 4:<
    """

    url = "/mgmt/inventory/exportInventorySumPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
