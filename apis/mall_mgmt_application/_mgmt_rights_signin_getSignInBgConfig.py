import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_getSignInBgConfig(headers=headers):
    """
    获取签到背景图片
    /mgmt/rights/signin/getSignInBgConfig
    """

    url = "/mgmt/rights/signin/getSignInBgConfig"
    with client.get(url=url, headers=headers) as r:
        return r
