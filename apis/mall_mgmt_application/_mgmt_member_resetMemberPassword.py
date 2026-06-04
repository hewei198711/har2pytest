import os

from util.client import client

data = {
    "id": 0,  # ID，主账号传会员ID，子账号传子账号ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_resetMemberPassword(data=data, headers=headers):
    """
    重置会员密码
    /mgmt/member/resetMemberPassword

    参数说明:
    - id: ID，主账号传会员ID，子账号传子账号ID
    """

    url = "/mgmt/member/resetMemberPassword"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
