import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_importGrantMemberTemplate(headers=headers):
    """
    派发用户导入模板下载
    /mgmt/prmt/couponGrant/importGrantMemberTemplate
    """

    url = "/mgmt/prmt/couponGrant/importGrantMemberTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
