import os

from util.client import client

params = {
    "businessId": "",  # 单号
    "createBegin": "",  # 出/入库开始时间
    "createEnd": "",  # 出/入库结束时间
    "outIn": 0,  # 出入库：1入库 2出库
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "sourceType": 0,  # 来源：1押货 2押货退货 3配送数量 4配送退回 5库存调整 6补单 12押货调整
    "产品编码": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_detailList(params=params, headers=headers):
    """
    库存明细
    /appStore/inventory/detailList

    参数说明:
    - businessId: 单号
    - createBegin: 出/入库开始时间
    - createEnd: 出/入库结束时间
    - outIn: 出入库：1入库 2出库
    - pageNum: 页数
    - pageSize: 页大小
    - sourceType: 来源：1押货 2押货退货 3配送数量 4配送退回 5库存调整 6补单 12押货调整
    """

    url = "/appStore/inventory/detailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
