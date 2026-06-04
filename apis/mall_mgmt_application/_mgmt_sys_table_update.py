import os

from util.client import client

data = {
    "channel": 0,  # 渠道:1.服务中心 2.商城 3.服务中心+商城
    "exampleImgUrl": "",  # 填写样例图片url
    "id": 0,  # 主键id
    "purpose": "",  # 用途
    "status": 0,  # 状态
    "tableName": "",  # 表格名称
    "tableTypeId": 0,  # 表格类型
    "uploadTableDoc": "",  # 上传文档
    "uploadTableDocName": "",  # 上传文件名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_table_update(data=data, headers=headers):
    """
    更新表格信息
    /mgmt/sys/table/update

    参数说明:
    - channel: 渠道:1.服务中心 2.商城 3.服务中心+商城
    - exampleImgUrl: 填写样例图片url
    - id: 主键id
    - purpose: 用途
    - status: 状态
    - tableName: 表格名称
    - tableTypeId: 表格类型
    - uploadTableDoc: 上传文档
    - uploadTableDocName: 上传文件名称
    """

    url = "/mgmt/sys/table/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
