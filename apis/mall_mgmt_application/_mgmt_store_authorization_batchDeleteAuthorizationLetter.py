import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_authorization_batchDeleteAuthorizationLetter(headers=headers):
    """
    批量删除授权书
    /mgmt/store/authorization/batchDeleteAuthorizationLetter
    """

    url = "/mgmt/store/authorization/batchDeleteAuthorizationLetter"
    with client.post(url=url, headers=headers) as r:
        return r
