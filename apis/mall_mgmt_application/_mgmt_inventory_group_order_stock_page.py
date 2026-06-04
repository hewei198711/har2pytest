import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "month": 0,  # 订单月份,格式:yyyyMM
    "orderNo": "",  # 团购单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "settleMonth": 0,  # 月结月份,格式:yyyyMM
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_stock_page(params=params, headers=headers):
    """
    分页查询团购单库存列表
    /mgmt/inventory/group-order/stock/page

    参数说明:
    - companyCode: 分公司编号
    - month: 订单月份,格式:yyyyMM
    - orderNo: 团购单编号
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - settleMonth: 月结月份,格式:yyyyMM
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/group-order/stock/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
