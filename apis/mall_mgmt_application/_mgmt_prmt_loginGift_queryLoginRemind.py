import os

from util.client import client

params = {
    "activityName": "",  # 登录提醒活动名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_queryLoginRemind(params=params, headers=headers):
    """
    查询登录提醒记录
    /mgmt/prmt/loginGift/queryLoginRemind

    参数说明:
    - activityName: 登录提醒活动名称
    """

    url = "/mgmt/prmt/loginGift/queryLoginRemind"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
