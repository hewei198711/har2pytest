import os

from util.client import client

params = {
    "id": "",  # 素材id
    "type": "",  # 0取消置顶 1置顶
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_cmsMaterialIsToppingById(params=params, headers=headers):
    """
    素材置顶/取消置顶
    /mgmt/cms/material/cmsMaterialIsToppingById

    参数说明:
    - id: 素材id
    - type: 0取消置顶 1置顶
    """

    url = "/mgmt/cms/material/cmsMaterialIsToppingById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
