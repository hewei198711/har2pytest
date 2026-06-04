import os

from util.client import client

data = {
    "ids": [],  # 主键ID集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_batchDelCmsMaterial(data=data, headers=headers):
    """
    批量删除素材
    /mgmt/cms/material/batchDelCmsMaterial

    参数说明:
    - ids: 主键ID集合
    """

    url = "/mgmt/cms/material/batchDelCmsMaterial"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
