import os

from util.client import client

data = {
    "id": 0,  # 主键Id
    "usable": 0,  # 是否可用：1-启用 2-禁用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_invite_editState(data=data, headers=headers):
    """
    启用与禁用
    /mgmt/rights/invite/editState

    参数说明:
    - id: 主键Id
    - usable: 是否可用：1-启用 2-禁用
    """

    url = "/mgmt/rights/invite/editState"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
