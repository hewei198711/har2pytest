import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_getImportErrorDataList(params=params, headers=headers):
    """
    导出导入错误门店列表
    /mgmt/prmt/couponTransfer/getImportErrorDataList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/couponTransfer/getImportErrorDataList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
