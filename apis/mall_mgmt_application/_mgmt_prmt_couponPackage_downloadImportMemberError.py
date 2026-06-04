import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_downloadImportMemberError(params=params, headers=headers):
    """
    下载导入失败用户列表
    /mgmt/prmt/couponPackage/downloadImportMemberError

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/couponPackage/downloadImportMemberError"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
