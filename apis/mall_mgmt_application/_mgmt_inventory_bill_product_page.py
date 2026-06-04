import os

from util.client import client

params = {
    "isBadAssetStore": 0,  # 是否不良资产门店, 0->否 1->是';
    "month": 0,  # 月份
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_bill_product_page(params=params, headers=headers):
    """
    分页查询库存历史列表（产品维度）
    /mgmt/inventory/bill/product/page

    参数说明:
    - isBadAssetStore: 是否不良资产门店, 0->否 1->是';
    - month: 月份
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    """

    url = "/mgmt/inventory/bill/product/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
