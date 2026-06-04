import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_verify(headers=headers):
    """
    85折手工录入流水单个审核
    /mgmt/inventory/disManualInputRemit/verify
    """

    url = "/mgmt/inventory/disManualInputRemit/verify"
    with client.get(url=url, headers=headers) as r:
        return r
