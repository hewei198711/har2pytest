import os

from util.client import client

params = {
    "combineBegin": "",  # 组合开始时间
    "combineEnd": "",  # 组合结束时间
    "companyCode": "",  # 分公司编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号/名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_record_export_excel(params=params, headers=headers):
    """
    导出套装组合记录列表
    /mgmt/dis-inventory/combine/record/export-excel

    参数说明:
    - combineBegin: 组合开始时间
    - combineEnd: 组合结束时间
    - companyCode: 分公司编号
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号/名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dis-inventory/combine/record/export-excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
