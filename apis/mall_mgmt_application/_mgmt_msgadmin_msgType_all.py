import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_msgType_all(headers=headers):
    """
    获取所有数据,子父级树形结构
    /mgmt/msgadmin/msgType/all
    """

    url = "/mgmt/msgadmin/msgType/all"
    with client.get(url=url, headers=headers) as r:
        return r
