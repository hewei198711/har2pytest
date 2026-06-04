import os

from util.client import client

params = {
    "id": "",  # 顾客ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getSubMemberById(params=params, headers=headers):
    """
    根据顾客ID获取顾客下所有子账号
    /mgmt/member/getSubMemberById

    参数说明:
    - id: 顾客ID
    """

    url = "/mgmt/member/getSubMemberById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
