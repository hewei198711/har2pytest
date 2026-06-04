import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_exportStoreDistributionTemplate(headers=headers):
    """
    押货分配量批量导入模板下载
    /mgmt/inventory/distribution/exportStoreDistributionTemplate
    """

    url = "/mgmt/inventory/distribution/exportStoreDistributionTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
