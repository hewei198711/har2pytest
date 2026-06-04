import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getImportErrorList(params=params, headers=headers):
    """
    下载导入错误列表
    /mgmt/prmt/couponGrant/getImportErrorList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/couponGrant/getImportErrorList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
