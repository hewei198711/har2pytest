import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
    "sourceType": 0,  # 入库类型：1押货 4顾客退货 5库存调整, 出库类型：2押货退货 3商城订单 5库存调整
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_export_stockOutDetailList(params=params, headers=headers):
    """
    导出出库明细
    /appStore/inventory/export/stockOutDetailList

    参数说明:
    - beginTime: 开始时间
    - endTime: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    - sourceType: 入库类型：1押货 4顾客退货 5库存调整, 出库类型：2押货退货 3商城订单 5库存调整
    """

    url = "/appStore/inventory/export/stockOutDetailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
