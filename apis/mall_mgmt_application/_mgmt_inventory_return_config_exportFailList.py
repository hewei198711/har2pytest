import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_exportFailList(headers=headers):
    """
    退货额度搜索列表导出失败记录
    /mgmt/inventory/return/config/exportFailList
    """

    url = "/mgmt/inventory/return/config/exportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
