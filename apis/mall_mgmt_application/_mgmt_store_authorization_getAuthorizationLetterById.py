import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_getAuthorizationLetterById(params=params, headers=headers):
    """
    根据ID查询授权书详情
    /mgmt/store/authorization/getAuthorizationLetterById

    参数说明:
    - id: id
    """

    url = "/mgmt/store/authorization/getAuthorizationLetterById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
