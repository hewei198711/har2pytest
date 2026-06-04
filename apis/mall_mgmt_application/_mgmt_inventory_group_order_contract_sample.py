import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_contract_sample(headers=headers):
    """
    获取合同范本下载地址
    /mgmt/inventory/group-order/contract-sample
    """

    url = "/mgmt/inventory/group-order/contract-sample"
    with client.get(url=url, headers=headers) as r:
        return r
