import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_exportStoreDistributionFailRecord(headers=headers):
    """
    押货分配量批量导入失败记录导出
    /mgmt/inventory/distribution/exportStoreDistributionFailRecord
    """

    url = "/mgmt/inventory/distribution/exportStoreDistributionFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r
