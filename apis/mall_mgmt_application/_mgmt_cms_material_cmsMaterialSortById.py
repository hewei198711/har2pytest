import os

from util.client import client

params = {
    "id": "",  # 素材id
    "sort": "",  # 排序序号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_cmsMaterialSortById(params=params, headers=headers):
    """
    素材排序
    /mgmt/cms/material/cmsMaterialSortById

    参数说明:
    - id: 素材id
    - sort: 排序序号
    """

    url = "/mgmt/cms/material/cmsMaterialSortById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
