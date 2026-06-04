import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_getSignInBgConfigEditLogList(params=params, headers=headers):
    """
    获取签到背景图片修改记录
    /mgmt/rights/signin/getSignInBgConfigEditLogList

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/mgmt/rights/signin/getSignInBgConfigEditLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
