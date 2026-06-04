import os

from util.client import client

data = {
    "mobile": "",  # 手机号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_addWhiteListUser(data=data, headers=headers):
    """
    新增单个白名单用户
    /mgmt/cms/whiteList/addWhiteListUser

    参数说明:
    - mobile: 手机号
    """

    url = "/mgmt/cms/whiteList/addWhiteListUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
