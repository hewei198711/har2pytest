import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_discredit_importBatch(headers=headers):
    """
    85%服务中心信誉额导入
    /mgmt/inventory/discredit/importBatch
    """

    url = "/mgmt/inventory/discredit/importBatch"
    with client.post(url=url, headers=headers) as r:
        return r
