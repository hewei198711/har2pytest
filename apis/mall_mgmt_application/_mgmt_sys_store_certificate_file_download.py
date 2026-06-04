import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_file_download(params=params, headers=headers):
    """
    公司证件文件下载
    /mgmt/sys/store/certificate/file/download

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/store/certificate/file/download"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
