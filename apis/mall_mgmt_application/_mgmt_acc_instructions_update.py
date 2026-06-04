import os

from util.client import client

data = {
    "id": 0,  # ID
    "instructionsContent": "",  # 内容
    "instructionsName": "",  # 名称
    "instructionsShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
    "serialNo": "",  # 关联产品编号
    "videoName": "",  # 视频名称
    "videoUrl": "",  # 视频地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_update(data=data, headers=headers):
    """
    编辑使用说明
    /mgmt/acc/instructions/update

    参数说明:
    - id: ID
    - instructionsContent: 内容
    - instructionsName: 名称
    - instructionsShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - serialNo: 关联产品编号
    - videoName: 视频名称
    - videoUrl: 视频地址
    """

    url = "/mgmt/acc/instructions/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
