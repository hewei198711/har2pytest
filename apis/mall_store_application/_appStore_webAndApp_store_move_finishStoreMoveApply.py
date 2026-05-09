import os

from util.client import client

data = {
    "completeMoveTime": "",  # 完成搬迁时间
    "id": 0,  # 主键id
    "newPic": [],  # 新门店装修照片
    "oldPic": [],  # 旧门店拆除照片
    "port": 0,  # 请求端 0后台 1APP 2PC
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_finishStoreMoveApply(data=data, headers=headers):
    """
    完成搬迁申请----web,app,后台
    /appStore/webAndApp/store/move/finishStoreMoveApply

    参数说明:
    - completeMoveTime: 完成搬迁时间
    - id: 主键id
    - newPic: 新门店装修照片
    - oldPic: 旧门店拆除照片
    - port: 请求端 0后台 1APP 2PC
    """

    url = "/appStore/webAndApp/store/move/finishStoreMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
