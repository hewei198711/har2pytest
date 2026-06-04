import os

from util.client import client

data = {
    "id": 0,  # 主账号ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_removeSubAccount(data=data, headers=headers):
    """
    删除关联账号(子账号)
    /mgmt/member/removeSubAccount

    参数说明:
    - id: 主账号ID
    """

    url = "/mgmt/member/removeSubAccount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
