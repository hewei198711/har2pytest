import os

from util.client import client

data = {
    "hotkeyName": "",  # TODO: 添加参数说明
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_addMaterialHotkey(data=data, headers=headers):
    """
    素材管理-新增热词
    /mgmt/cms/material/addMaterialHotkey

    参数说明:
    - sort: 排序
    """

    url = "/mgmt/cms/material/addMaterialHotkey"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
