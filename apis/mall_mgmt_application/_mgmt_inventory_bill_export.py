import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "filterShopType": 0,  # 是否过滤网点类型：0否 1是
    "maxMonth": 0,  # 月份最大值,格式：yyyyMM
    "minMonth": 0,  # 月份最小值,格式：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_bill_export(params=params, headers=headers):
    """
    excel导出库存对账单
    /mgmt/inventory/bill/export

    参数说明:
    - companyCode: 分公司编号
    - filterShopType: 是否过滤网点类型：0否 1是
    - maxMonth: 月份最大值,格式：yyyyMM
    - minMonth: 月份最小值,格式：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/bill/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
