import os

from util.client import client

params = {
    "beginMonth": 0,  # 月份，格式为：yyyyMM
    "catalogId": 0,  # 产品类型（商品分类Id）
    "endMonth": 0,  # 月份，格式为：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码/名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_dis_inventory_bill_book_page(params=params, headers=headers):
    """
    查询库存月结台账
    /appStore/dis-inventory/bill/book/page

    参数说明:
    - beginMonth: 月份，格式为：yyyyMM
    - catalogId: 产品类型（商品分类Id）
    - endMonth: 月份，格式为：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码/名称
    """

    url = "/appStore/dis-inventory/bill/book/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
