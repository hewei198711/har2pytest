import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_batchImportTemplateFor13(headers=headers):
    """
    1:3手工录入流水批量导入模板下载
    /mgmt/inventory/remit/batchImportTemplateFor13
    """

    url = "/mgmt/inventory/remit/batchImportTemplateFor13"
    with client.get(url=url, headers=headers) as r:
        return r
