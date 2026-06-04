import os

from util.client import client

data = {
    "id": 0,  # id
    "status": 0,  # 状态,0:待上架;1:已上架;2:已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_changeStatus(data=data, headers=headers):
    """
    icon上下架
    /mgmt/cms/iconSetting/changeStatus

    参数说明:
    - id: id
    - status: 状态,0:待上架;1:已上架;2:已下架
    """

    url = "/mgmt/cms/iconSetting/changeStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
