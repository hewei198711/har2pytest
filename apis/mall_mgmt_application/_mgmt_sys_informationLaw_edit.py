import os

from util.client import client

data = {
    "fileUrl": "",  # 文件url
    "id": 0,  # 法规咨询id, 空代表新增法规, 非空则为编辑法规
    "status": 0,  # 状态 1->启用 2->禁用
    "title": "",  # 法规名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_informationLaw_edit(data=data, headers=headers):
    """
    法规咨询(新)-编辑
    /mgmt/sys/informationLaw/edit

    参数说明:
    - fileUrl: 文件url
    - id: 法规咨询id, 空代表新增法规, 非空则为编辑法规
    - status: 状态 1->启用 2->禁用
    - title: 法规名称
    """

    url = "/mgmt/sys/informationLaw/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
