import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_return_config_excelBatchImport(headers=headers):
    """
    退货额度Excel批量导入
    /mgmt/inventory/return/config/excelBatchImport
    """

    url = "/mgmt/inventory/return/config/excelBatchImport"
    with client.post(url=url, headers=headers) as r:
        return r
