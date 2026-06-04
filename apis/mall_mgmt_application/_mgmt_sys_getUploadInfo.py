import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getUploadInfo(headers=headers):
    """
    返回需要上传的oss信息
    /mgmt/sys/getUploadInfo
    """

    url = "/mgmt/sys/getUploadInfo"
    with client.get(url=url, headers=headers) as r:
        return r
