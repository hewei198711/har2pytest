import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "type": 0,  # 类型 1：首次;2:最后一次
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userLoginLog_getUserLoginGroupByClient(params=params, headers=headers):
    """
    用户登录日志各端(首次/最后一次)
    /mgmt/dataAdmin/userLoginLog/getUserLoginGroupByClient

    参数说明:
    - cardNo: 会员卡号
    - type: 类型 1：首次;2:最后一次
    """

    url = "/mgmt/dataAdmin/userLoginLog/getUserLoginGroupByClient"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
