import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_exportMemberTemplate(headers=headers):
    """
    用户导入模板下载
    /mgmt/prmt/couponPackage/exportMemberTemplate
    """

    url = "/mgmt/prmt/couponPackage/exportMemberTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
