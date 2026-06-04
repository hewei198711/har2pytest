import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getCompanyList(headers=headers):
    """
    获取分公司列表
    /mgmt/inventory/common/getCompanyList
    """

    url = "/mgmt/inventory/common/getCompanyList"
    with client.get(url=url, headers=headers) as r:
        return r
