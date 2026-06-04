import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getFileUploadInfo(headers=headers):
    """
    oss文件上传返回签名相关信息接口
    /mgmt/store/getFileUploadInfo
    """

    url = "/mgmt/store/getFileUploadInfo"
    with client.get(url=url, headers=headers) as r:
        return r
