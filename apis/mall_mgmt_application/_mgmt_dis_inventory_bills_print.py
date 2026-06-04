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


def _mgmt_dis_inventory_bills_print(params=params, headers=headers):
    """
    打印库存对账单
    /mgmt/dis-inventory/bills/print

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

    url = "/mgmt/dis-inventory/bills/print"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
