import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_check_listYearQuarter(headers=headers):
    """
    列出所有已生成的年季
    /mgmt/inventory/check/listYearQuarter
    """

    url = "/mgmt/inventory/check/listYearQuarter"
    with client.get(url=url, headers=headers) as r:
        return r
