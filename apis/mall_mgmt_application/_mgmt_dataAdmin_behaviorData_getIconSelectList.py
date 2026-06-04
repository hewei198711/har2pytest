import os

from util.client import client

params = {
    "includeAll": "",  # 是否包含全部 0/null 否 1.是
    "location": "",  # 显示位置，1：PC商城首页，2：APP，3：小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getIconSelectList(params=params, headers=headers):
    """
    查询首页icon下拉框列表
    /mgmt/dataAdmin/behaviorData/getIconSelectList

    参数说明:
    - includeAll: 是否包含全部 0/null 否 1.是
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    """

    url = "/mgmt/dataAdmin/behaviorData/getIconSelectList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
