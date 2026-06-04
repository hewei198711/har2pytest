import os

from util.client import client

data = {
    "switchStatus": 0,  # 白名单开关状态:0.关 1.开
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_jzhfAuthCheckSwitch(data=data, headers=headers):
    """
    精准护肤白名单检测开关
    /mgmt/cms/whiteList/jzhfAuthCheckSwitch

    参数说明:
    - switchStatus: 白名单开关状态:0.关 1.开
    """

    url = "/mgmt/cms/whiteList/jzhfAuthCheckSwitch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
