import os

from util.client import client

data = {
    "id": 0,  # 顾客ID
    "memberStatus": 0,  # 要修改成的会员状态标识
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_changeMemberStatus(data=data, headers=headers):
    """
    修改会员账号状态
    /mgmt/member/changeMemberStatus

    参数说明:
    - id: 顾客ID
    - memberStatus: 要修改成的会员状态标识
    """

    url = "/mgmt/member/changeMemberStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
