import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_common_fetchFreightTemplate(headers=headers):
    """
    获取最新的运费计算模板
    /mgmt/inventory/dis/mortgage/common/fetchFreightTemplate
    """

    url = "/mgmt/inventory/dis/mortgage/common/fetchFreightTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
