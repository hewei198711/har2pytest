import os

from util.client import client

params = {
    "id": "",  # 顾客ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getMemberInfoById(params=params, headers=headers):
    """
    根据顾客ID获取顾客详细信息
    /mgmt/member/getMemberInfoById

    参数说明:
    - id: 顾客ID
    """

    url = "/mgmt/member/getMemberInfoById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
