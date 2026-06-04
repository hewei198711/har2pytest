import os

from util.client import client

params = {
    "materialId": 0,  # 物料ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_downloadRecord_save(params=params, headers=headers):
    """
    保存下载记录
    /mgmt/sys/material/downloadRecord/save

    参数说明:
    - materialId: 物料ID
    """

    url = "/mgmt/sys/material/downloadRecord/save"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
