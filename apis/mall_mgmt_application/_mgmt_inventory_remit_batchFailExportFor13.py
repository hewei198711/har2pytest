import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_batchFailExportFor13(headers=headers):
    """
    1:3手工录入流水导入失败记录导出
    /mgmt/inventory/remit/batchFailExportFor13
    """

    url = "/mgmt/inventory/remit/batchFailExportFor13"
    with client.get(url=url, headers=headers) as r:
        return r
