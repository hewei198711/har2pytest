import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_fetchProductProvenance(headers=headers):
    """
    获取商品产地信息列表
    /mgmt/inventory/common/fetchProductProvenance
    """

    url = "/mgmt/inventory/common/fetchProductProvenance"
    with client.get(url=url, headers=headers) as r:
        return r
