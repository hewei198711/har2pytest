import os

from util.client import client

params = {
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_listNotDeliverProductForStore(params=params, headers=headers):
    """
    久欠未发货明细(服务中心)
    /appStore/inventory/listNotDeliverProductForStore

    参数说明:
    - endTime: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    - startTime: 开始时间
    """

    url = "/appStore/inventory/listNotDeliverProductForStore"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
