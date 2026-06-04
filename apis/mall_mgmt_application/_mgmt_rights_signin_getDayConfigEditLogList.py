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


def _mgmt_rights_signin_getDayConfigEditLogList(params=params, headers=headers):
    """
    查询每日签到奖励配置修改记录列表
    /mgmt/rights/signin/getDayConfigEditLogList

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/mgmt/rights/signin/getDayConfigEditLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
