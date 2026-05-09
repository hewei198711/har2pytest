import os

from util.client import client

data = {
    "newMobile": "",  # 新电话号码
    "oldMobile": "",  # 原电话号码
    "type": 0,  # 类型，1/服务中心电话1, 2/服务中心电话2
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyServiceMobileChange(data=data, headers=headers):
    """
    申请服务中心手机号变更(直接通过，不需要审核)
    /appStore/store/profile/applyServiceMobileChange

    参数说明:
    - newMobile: 新电话号码
    - oldMobile: 原电话号码
    - type: 类型，1/服务中心电话1, 2/服务中心电话2
    """

    url = "/appStore/store/profile/applyServiceMobileChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
