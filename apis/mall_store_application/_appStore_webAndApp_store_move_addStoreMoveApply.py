import os

from util.client import client

data = {
    "infoDto": "",  # 搬迁店铺详细信息
    "movePicDto": "",  # 搬迁相关图
    "storeMoveDto": "",  # 搬迁申请信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_webAndApp_store_move_addStoreMoveApply(data=data, headers=headers):
    """
    添加搬迁申请记录(成功的话返回id)--web,app
    /appStore/webAndApp/store/move/addStoreMoveApply

    参数说明:
    - infoDto: 搬迁店铺详细信息
    - movePicDto: 搬迁相关图
    - storeMoveDto: 搬迁申请信息
    """

    url = "/appStore/webAndApp/store/move/addStoreMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
