import os

from util.client import client

data = {
    "wechat": "",  # 微信号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyWechatChange(data=data, headers=headers):
    """
    申请微信号信息变更(直接通过，不需要审核)
    /appStore/store/profile/applyWechatChange

    参数说明:
    - wechat: 微信号
    """

    url = "/appStore/store/profile/applyWechatChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
