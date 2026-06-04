import os

from util.client import client

params = {
    "displayUserSerial": "",  # 素材展示用户关联序列号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_exportMaterialDisplayUserFailList(params=params, headers=headers):
    """
    导出素材展示用户导入失败原因列表
    /mgmt/cms/material/exportMaterialDisplayUserFailList

    参数说明:
    - displayUserSerial: 素材展示用户关联序列号
    """

    url = "/mgmt/cms/material/exportMaterialDisplayUserFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
