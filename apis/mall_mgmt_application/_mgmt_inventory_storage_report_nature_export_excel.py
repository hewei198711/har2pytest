import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "reportRangeType": 0,  # 月份选择类型
    "shopCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_storage_report_nature_export_excel(params=params, headers=headers):
    """
    excel导出自然月份库存对账单（历史）列表
    /mgmt/inventory/storage-report-nature/export-excel

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - reportRangeType: 月份选择类型
    - shopCode: 服务中心编号
    """

    url = "/mgmt/inventory/storage-report-nature/export-excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
