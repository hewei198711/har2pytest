import os

from util.client import client

params = {
    "id": 0,  # id
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_getMoveApplyRecord(params=params, headers=headers):
    """
    查询该服务中心的最新申请记录的搬迁操作记录
    /appStore/webAndApp/store/move/getMoveApplyRecord

    参数说明:
    - id: id
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/appStore/webAndApp/store/move/getMoveApplyRecord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
