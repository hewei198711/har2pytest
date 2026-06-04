import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_batchImportTemplate(headers=headers):
    """
    85折手工录入流水批量导入模板下载
    /mgmt/inventory/disManualInputRemit/batchImportTemplate
    """

    url = "/mgmt/inventory/disManualInputRemit/batchImportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
