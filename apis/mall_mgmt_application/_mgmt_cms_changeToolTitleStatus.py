import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_changeToolTitleStatus(data=data, headers=headers):
    """
    工具PC类型标题状态变更
    /mgmt/cms/changeToolTitleStatus

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/changeToolTitleStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
