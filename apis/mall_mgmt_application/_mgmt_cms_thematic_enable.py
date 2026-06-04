import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_thematic_enable(data=data, headers=headers):
    """
    专题页启用/禁用
    /mgmt/cms/thematic/enable

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/thematic/enable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
