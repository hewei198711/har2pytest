import os

from util.client import client

data = {
    "channelsId": "",  # 视频号id
    "channelsName": "",  # 视频号名称
    "loginMobile": "",  # 登陆手机号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_updateAlreadySignUpInfo(data=data, headers=headers):
    """
    更新已报名信息
    /mgmt/cms/kos/updateAlreadySignUpInfo

    参数说明:
    - channelsId: 视频号id
    - channelsName: 视频号名称
    - loginMobile: 登陆手机号
    """

    url = "/mgmt/cms/kos/updateAlreadySignUpInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
