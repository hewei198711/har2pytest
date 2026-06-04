import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_generateImportKey(headers=headers):
    """
    生成importKey:新增页面导入与手动添加用户需要携带
    /mgmt/prmt/couponPackage/generateImportKey
    """

    url = "/mgmt/prmt/couponPackage/generateImportKey"
    with client.get(url=url, headers=headers) as r:
        return r
