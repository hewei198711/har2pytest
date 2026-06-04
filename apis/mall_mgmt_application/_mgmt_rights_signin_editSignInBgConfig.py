import os

from util.client import client

params = {
    "bgUrl": "",  # 背景图片链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_editSignInBgConfig(params=params, headers=headers):
    """
    修改签到背景图片
    /mgmt/rights/signin/editSignInBgConfig

    参数说明:
    - bgUrl: 背景图片链接
    """

    url = "/mgmt/rights/signin/editSignInBgConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
