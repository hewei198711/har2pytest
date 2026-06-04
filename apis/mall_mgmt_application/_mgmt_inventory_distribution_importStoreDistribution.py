import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_distribution_importStoreDistribution(headers=headers):
    """
    押货分配量批量导入
    /mgmt/inventory/distribution/importStoreDistribution
    """

    url = "/mgmt/inventory/distribution/importStoreDistribution"
    with client.post(url=url, headers=headers) as r:
        return r
