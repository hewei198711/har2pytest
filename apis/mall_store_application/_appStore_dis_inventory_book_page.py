import os

from util.client import client

params = {
    "catalogId": 0,  # 产品类型（商品分类Id）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_dis_inventory_book_page(params=params, headers=headers):
    """
    查询实时库存台账
    /appStore/dis-inventory/book/page

    参数说明:
    - catalogId: 产品类型（商品分类Id）
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码/名称
    """

    url = "/appStore/dis-inventory/book/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
