import os

from util.client import client

data = {
    "baId": 0,  # 行为数据分析总表id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_behaviorData_home_getBrowsePathList(data=data, headers=headers):
    """
    首页顾客浏览路径
    /mgmt/dataAdmin/behaviorData/home/getBrowsePathList

    参数说明:
    - baId: 行为数据分析总表id
    """

    url = "/mgmt/dataAdmin/behaviorData/home/getBrowsePathList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
