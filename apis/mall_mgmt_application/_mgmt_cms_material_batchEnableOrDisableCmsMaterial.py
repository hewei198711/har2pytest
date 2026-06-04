import os

from util.client import client

data = {
    "ids": [],  # 主键ID集合
    "status": 0,  # 状态 1：启用（默认）0：禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_batchEnableOrDisableCmsMaterial(data=data, headers=headers):
    """
    批量启用/禁用素材
    /mgmt/cms/material/batchEnableOrDisableCmsMaterial

    参数说明:
    - ids: 主键ID集合
    - status: 状态 1：启用（默认）0：禁用
    """

    url = "/mgmt/cms/material/batchEnableOrDisableCmsMaterial"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
