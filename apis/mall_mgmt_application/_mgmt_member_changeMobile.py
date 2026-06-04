import os

from util.client import client

data = {
    "id": 0,  # 顾客ID
    "mobile": "",  # 新手机号码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_changeMobile(data=data, headers=headers):
    """
    修改注册手机号码
    /mgmt/member/changeMobile

    参数说明:
    - id: 顾客ID
    - mobile: 新手机号码
    """

    url = "/mgmt/member/changeMobile"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
