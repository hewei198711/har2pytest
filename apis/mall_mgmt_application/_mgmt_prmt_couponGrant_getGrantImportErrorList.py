import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getGrantImportErrorList(params=params, headers=headers):
    """
    查询导入错误列表，派发导入
    /mgmt/prmt/couponGrant/getGrantImportErrorList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/couponGrant/getGrantImportErrorList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
