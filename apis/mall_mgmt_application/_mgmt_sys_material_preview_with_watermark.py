import os

from util.client import client

params = {
    "materialId": 0,  # materialId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_preview_with_watermark(params=params, headers=headers):
    """
    预览形象物料（带水印）
    /mgmt/sys/material/preview/with-watermark

    参数说明:
    - materialId: materialId
    """

    url = "/mgmt/sys/material/preview/with-watermark"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
