import os

from util.client import client

params = {
    "id": 0,  # id
    "storeCode": "",  # 服务中心编号
    "type": 0,  # 预览或者下载形象手册:1预览 2下载
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_image_manual_download(params=params, headers=headers):
    """
    形象手册下载
    /mgmt/sys/image/manual/download

    参数说明:
    - id: id
    - storeCode: 服务中心编号
    - type: 预览或者下载形象手册:1预览 2下载
    """

    url = "/mgmt/sys/image/manual/download"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
