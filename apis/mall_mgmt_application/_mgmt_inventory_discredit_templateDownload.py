import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_discredit_templateDownload(headers=headers):
    """
    85%信誉额批量调整模板下载
    /mgmt/inventory/discredit/templateDownload
    """

    url = "/mgmt/inventory/discredit/templateDownload"
    with client.get(url=url, headers=headers) as r:
        return r
