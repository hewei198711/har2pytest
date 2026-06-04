import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_changeToolStatus(data=data, headers=headers):
    """
    工具状态变更
    /mgmt/cms/changeToolStatus

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/changeToolStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
