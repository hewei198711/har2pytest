import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_updateMaterialHotkeySort(data=data, headers=headers):
    """
    素材管理-搜索热词排序
    /mgmt/cms/material/updateMaterialHotkeySort

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/material/updateMaterialHotkeySort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
