import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_returnConfigTemplateDownLaod(headers=headers):
    """
    退货额度批量导入模板下载
    /mgmt/inventory/return/config/returnConfigTemplateDownLaod
    """

    url = "/mgmt/inventory/return/config/returnConfigTemplateDownLaod"
    with client.get(url=url, headers=headers) as r:
        return r
