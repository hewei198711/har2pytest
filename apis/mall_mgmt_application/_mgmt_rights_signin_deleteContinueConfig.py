import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_deleteContinueConfig(params=params, headers=headers):
    """
    删除连续累计签到奖励配置
    /mgmt/rights/signin/deleteContinueConfig

    参数说明:
    - id: id
    """

    url = "/mgmt/rights/signin/deleteContinueConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
