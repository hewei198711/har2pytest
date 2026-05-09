import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getFileUploadInfo(headers=headers):
    """
    oss文件上传返回签名相关信息接口
    /appStore/common/getFileUploadInfo
    """

    url = "/appStore/common/getFileUploadInfo"
    with client.get(url=url, headers=headers) as r:
        return r
