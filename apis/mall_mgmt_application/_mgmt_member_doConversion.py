import os

from util.client import client

data = {
    "id": 0,  # 顾客ID
    "toMemberType": 0,  # 目标身份标识
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_doConversion(data=data, headers=headers):
    """
    执行身份转换
    /mgmt/member/doConversion

    参数说明:
    - id: 顾客ID
    - toMemberType: 目标身份标识
    """

    url = "/mgmt/member/doConversion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
