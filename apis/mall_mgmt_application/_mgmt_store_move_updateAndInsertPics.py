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


def _mgmt_store_move_updateAndInsertPics(data=data, headers=headers):
    """
    上传/编辑新旧门店图片----后台
    /mgmt/store/move/updateAndInsertPics

    参数说明:
    - completeMoveTime: 完成搬迁时间
    - id: 主键id
    - newPic: 新门店装修照片
    - oldPic: 旧门店拆除照片
    - port: 请求端 0后台 1APP 2PC
    """

    url = "/mgmt/store/move/updateAndInsertPics"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
