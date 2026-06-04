import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getFileUploadInfo(headers=headers):
    """
    oss文件上传返回签名相关信息接口
    /mgmt/inventory/common/getFileUploadInfo
    """

    url = "/mgmt/inventory/common/getFileUploadInfo"
    with client.get(url=url, headers=headers) as r:
        return r
