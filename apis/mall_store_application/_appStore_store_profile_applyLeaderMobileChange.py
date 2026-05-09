import os

from util.client import client

data = {
    "newMobile": "",  # 新电话号码
    "newSmsCode": "",  # 新手机号码验证码
    "oldMobile": "",  # 原电话号码
    "oldSmsCode": "",  # 原手机号码验证码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyLeaderMobileChange(data=data, headers=headers):
    """
    申请负责人手机号变更(直接通过，不需要审核)
    /appStore/store/profile/applyLeaderMobileChange

    参数说明:
    - newMobile: 新电话号码
    - newSmsCode: 新手机号码验证码
    - oldMobile: 原电话号码
    - oldSmsCode: 原手机号码验证码
    """

    url = "/appStore/store/profile/applyLeaderMobileChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
