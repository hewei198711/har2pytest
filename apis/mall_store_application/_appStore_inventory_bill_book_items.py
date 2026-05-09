import os

from util.client import client

params = {
    "beginMonth": 0,  # 月份，格式为：yyyyMM
    "endMonth": 0,  # 月份，格式为：yyyyMM
    "productCode": "",  # 产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_bill_book_items(params=params, headers=headers):
    """
    查询库存月结台账明细
    /appStore/inventory/bill/book-items

    参数说明:
    - beginMonth: 月份，格式为：yyyyMM
    - endMonth: 月份，格式为：yyyyMM
    - productCode: 产品编号
    """

    url = "/appStore/inventory/bill/book-items"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
