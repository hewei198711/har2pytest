import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_getProfileChangeWaitStatus(headers=headers):
    """
    查询用户是否存在审核中的资料变更数据
    /appStore/store/profile/getProfileChangeWaitStatus
    """

    url = "/appStore/store/profile/getProfileChangeWaitStatus"
    with client.get(url=url, headers=headers) as r:
        return r
