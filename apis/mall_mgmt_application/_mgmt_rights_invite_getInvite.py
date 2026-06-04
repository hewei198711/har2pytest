import os

from util.client import client

params = {
    "id": "",  # 任务id
    "isEdit": False,  # 是否为编辑
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_invite_getInvite(params=params, headers=headers):
    """
    获取拉新任务信息(详情或编辑回显)
    /mgmt/rights/invite/getInvite

    参数说明:
    - id: 任务id
    - isEdit: 是否为编辑
    """

    url = "/mgmt/rights/invite/getInvite"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
