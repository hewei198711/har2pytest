import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_modelChangeTemplateDownload(headers=headers):
    """
    经营模式切换批量导入模板下载
    /mgmt/inventory/disManageModelChange/modelChangeTemplateDownload
    """

    url = "/mgmt/inventory/disManageModelChange/modelChangeTemplateDownload"
    with client.get(url=url, headers=headers) as r:
        return r
