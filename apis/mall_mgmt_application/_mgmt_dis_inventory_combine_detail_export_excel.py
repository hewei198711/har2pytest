import os

from util.client import client

data = {
    "combineIds": [],  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_detail_export_excel(data=data, headers=headers):
    """
    导出套装组合明细
    /mgmt/dis-inventory/combine/detail/export-excel
    """

    url = "/mgmt/dis-inventory/combine/detail/export-excel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
