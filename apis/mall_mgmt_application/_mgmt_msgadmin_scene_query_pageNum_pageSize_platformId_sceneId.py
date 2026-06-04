import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "platformId": 0,  # platformId
    "sceneId": 0,  # sceneId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_scene_query_pageNum_pageSize_platformId_sceneId(params=params, headers=headers):
    """
    系统消息管理-场景大类-操作查看接口
    /mgmt/msgadmin/scene/query/{pageNum}/{pageSize}/{platformId}/{sceneId}

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - platformId: platformId
    - sceneId: sceneId
    """

    url = f"/mgmt/msgadmin/scene/query/{params['pageNum']}/{params['pageSize']}/{params['platformId']}/{params['sceneId']}"
    with client.get(url=url, headers=headers) as r:
        return r
