import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_couponPackage_importMember(headers=headers):
    """
    导入派发顾客
    /mgmt/prmt/couponPackage/importMember
    """

    url = "/mgmt/prmt/couponPackage/importMember"
    with client.post(url=url, headers=headers) as r:
        return r
