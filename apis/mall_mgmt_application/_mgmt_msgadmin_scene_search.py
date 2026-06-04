import os

from util.client import client

params = {
    "name": "",  # name
    "platformId": 0,  # platformId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_scene_search(params=params, headers=headers):
    """
    系统消息管理-场景大类查询接口
    /mgmt/msgadmin/scene/search

    参数说明:
    - name: name
    - platformId: platformId
    """

    url = "/mgmt/msgadmin/scene/search"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
