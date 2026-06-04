import os

from util.client import client

params = {
    "fieldDescs": "",  # fieldDescs
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_downTemplate(params=params, headers=headers):
    """
    下载导入名单模版
    /mgmt/msgadmin/handmade/downTemplate

    参数说明:
    - fieldDescs: fieldDescs
    """

    url = "/mgmt/msgadmin/handmade/downTemplate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
