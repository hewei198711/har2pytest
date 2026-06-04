import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_discredit_exportFailRecord(headers=headers):
    """
    85%信誉额批量调整导入失败记录导出
    /mgmt/inventory/discredit/exportFailRecord
    """

    url = "/mgmt/inventory/discredit/exportFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r
