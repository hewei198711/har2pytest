import os

from util.client import client

params = {
    "mobile": "",  # mobile
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_clerk_checkMobile(params=params, headers=headers):
    """
    检查手机号码是否重复
    /appStore/store/clerk/checkMobile

    参数说明:
    - mobile: mobile
    """

    url = "/appStore/store/clerk/checkMobile"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
