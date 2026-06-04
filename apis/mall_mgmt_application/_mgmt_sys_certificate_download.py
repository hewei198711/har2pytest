import os

from util.client import client

params = {
    "id": 0,  # id
    "type": 0,  # 1预览 2下载
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_certificate_download(params=params, headers=headers):
    """
    公司证件下载
    /mgmt/sys/certificate/download

    参数说明:
    - id: id
    - type: 1预览 2下载
    """

    url = "/mgmt/sys/certificate/download"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
