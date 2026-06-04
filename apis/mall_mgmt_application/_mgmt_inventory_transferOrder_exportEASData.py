import os

from util.client import client

params = {
    "month": "",  # month
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_transferOrder_exportEASData(params=params, headers=headers):
    """
    导出EAS凭证
    /mgmt/inventory/transferOrder/exportEASData

    参数说明:
    - month: month
    """

    url = "/mgmt/inventory/transferOrder/exportEASData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
