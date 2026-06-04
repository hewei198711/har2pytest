import os

from util.client import client

data = {
    "hotkeyName": "",  # TODO: 添加参数说明
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_updateMaterialHotkeyInfo(data=data, headers=headers):
    """
    素材管理-编辑热词
    /mgmt/cms/material/updateMaterialHotkeyInfo

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/material/updateMaterialHotkeyInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
