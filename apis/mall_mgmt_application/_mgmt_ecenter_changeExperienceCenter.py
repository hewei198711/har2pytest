import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "status": 0,  # 状态，1：启用；2：禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_ecenter_changeExperienceCenter(data=data, headers=headers):
    """
    启用/禁用体验中心
    /mgmt/ecenter/changeExperienceCenter

    参数说明:
    - id: 主键id
    - status: 状态，1：启用；2：禁用
    """

    url = "/mgmt/ecenter/changeExperienceCenter"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
