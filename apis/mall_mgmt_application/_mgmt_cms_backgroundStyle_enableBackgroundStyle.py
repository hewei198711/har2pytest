import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_enableBackgroundStyle(data=data, headers=headers):
    """
    修改背景样式启用状态
    /mgmt/cms/backgroundStyle/enableBackgroundStyle

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/backgroundStyle/enableBackgroundStyle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
