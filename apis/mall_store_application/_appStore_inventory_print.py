import os

from util.client import client

params = {
    "catalogId": 0,  # 产品类型（商品分类Id）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
    "showId": 0,  # 产品前端分类id
    "sortDirection": 0,  # 排序方向，1.倒序，2.正序
    "sortType": 0,  # 排序方式，1.产品编码,2.按当前库存,3.按押货价合计
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_print(params=params, headers=headers):
    """
    打印库存单
    /appStore/inventory/print

    参数说明:
    - catalogId: 产品类型（商品分类Id）
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    - showId: 产品前端分类id
    - sortDirection: 排序方向，1.倒序，2.正序
    - sortType: 排序方式，1.产品编码,2.按当前库存,3.按押货价合计
    """

    url = "/appStore/inventory/print"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
