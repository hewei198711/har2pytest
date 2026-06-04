import os

from util.client import client

params = {
    "includeAll": "",  # 是否包含全部 0/null 否 1.是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_getThematicBarSelectList(params=params, headers=headers):
    """
    查询专题页下拉框列表
    /mgmt/dataAdmin/behaviorData/getThematicBarSelectList

    参数说明:
    - includeAll: 是否包含全部 0/null 否 1.是
    """

    url = "/mgmt/dataAdmin/behaviorData/getThematicBarSelectList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
