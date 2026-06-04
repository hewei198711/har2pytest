import os

from util.client import client

params = {
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_invite_getInvitePage(params=params, headers=headers):
    """
    分页查询拉新奖励
    /mgmt/rights/invite/getInvitePage

    参数说明:
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/rights/invite/getInvitePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
