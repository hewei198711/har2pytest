import os

from util.client import client

params = {
    "beginMonth": 0,  # 月份，格式为：yyyyMM
    "catalogId": 0,  # 产品类型（商品分类Id）
    "companyCode": "",  # 分公司编号
    "endMonth": 0,  # 月份，格式为：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码/名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_bill_book_items(params=params, headers=headers):
    """
    查询库存月结台账明细
    /mgmt/dis-inventory/bill/book-items

    参数说明:
    - beginMonth: 月份，格式为：yyyyMM
    - catalogId: 产品类型（商品分类Id）
    - companyCode: 分公司编号
    - endMonth: 月份，格式为：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码/名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dis-inventory/bill/book-items"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
