import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_exportFailList(headers=headers):
    """
    经营模式切换导出失败记录
    /mgmt/inventory/disManageModelChange/exportFailList
    """

    url = "/mgmt/inventory/disManageModelChange/exportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
