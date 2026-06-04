import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_getDayConfig(headers=headers):
    """
    查询每日签到奖励配置
    /mgmt/rights/signin/getDayConfig
    """

    url = "/mgmt/rights/signin/getDayConfig"
    with client.get(url=url, headers=headers) as r:
        return r
