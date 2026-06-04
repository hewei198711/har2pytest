import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_downloadImportFailPermission(params=params, headers=headers):
    """
    下载KOS转分权限导入失败列表
    /mgmt/weshop/downloadImportFailPermission

    参数说明:
    - key: key
    """

    url = "/mgmt/weshop/downloadImportFailPermission"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
