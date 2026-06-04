import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "shopCode": "",  # 服务中心编号
    "snapshotMonth": "",  # 月份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_storage_snapshot_export_excel(params=params, headers=headers):
    """
    excel导出库存对账单（历史）列表
    /mgmt/inventory/storage-snapshot/export-excel

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - shopCode: 服务中心编号
    - snapshotMonth: 月份
    """

    url = "/mgmt/inventory/storage-snapshot/export-excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
