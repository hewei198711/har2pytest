import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_exportPermissionTemplate(headers=headers):
    """
    导入模板下载
    /mgmt/weshop/exportPermissionTemplate
    """

    url = "/mgmt/weshop/exportPermissionTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
