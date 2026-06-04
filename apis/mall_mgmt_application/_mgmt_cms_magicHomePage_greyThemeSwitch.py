import os

from util.client import client

data = {
    "greyThemeSwitch": 0,  # 置灰开关: 1.开启 0.关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_greyThemeSwitch(data=data, headers=headers):
    """
    置灰开关操作
    /mgmt/cms/magicHomePage/greyThemeSwitch

    参数说明:
    - greyThemeSwitch: 置灰开关: 1.开启 0.关闭
    """

    url = "/mgmt/cms/magicHomePage/greyThemeSwitch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
