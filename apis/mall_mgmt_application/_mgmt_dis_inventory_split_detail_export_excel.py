import os

from util.client import client

params = {
    "id": 0,  # 拆分id
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_detail_export_excel(params=params, headers=headers):
    """
    导出套装拆分明细
    /mgmt/dis-inventory/split/detail/export-excel

    参数说明:
    - id: 拆分id
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 店铺编号
    """

    url = "/mgmt/dis-inventory/split/detail/export-excel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
