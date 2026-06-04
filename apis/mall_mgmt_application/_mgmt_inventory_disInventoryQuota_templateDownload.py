import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_templateDownload(headers=headers):
    """
    批量导入模板下载
    /mgmt/inventory/disInventoryQuota/templateDownload
    """

    url = "/mgmt/inventory/disInventoryQuota/templateDownload"
    with client.get(url=url, headers=headers) as r:
        return r
