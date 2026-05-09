import os

from util.client import client

data = {
    "adminIdCard": "",  # 管理员身份证
    "adminMobile": "",  # 管理员手机号
    "adminName": "",  # 管理员姓名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyCertChange(data=data, headers=headers):
    """
    申请电子印章企业认证信息变更
    /appStore/store/profile/applyCertChange

    参数说明:
    - adminIdCard: 管理员身份证
    - adminMobile: 管理员手机号
    - adminName: 管理员姓名
    """

    url = "/appStore/store/profile/applyCertChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
