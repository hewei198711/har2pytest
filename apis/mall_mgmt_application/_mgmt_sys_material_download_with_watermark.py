import os

from util.client import client

params = {
    "materialId": 0,  # materialId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_material_download_with_watermark(params=params, headers=headers):
    """
    带水印下载形象物料
    /mgmt/sys/material/download/with-watermark

    参数说明:
    - materialId: materialId
    """

    url = "/mgmt/sys/material/download/with-watermark"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
