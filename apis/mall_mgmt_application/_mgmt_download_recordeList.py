import os

from util.client import client

data = {
    "pageNum": 0,  # 分页查询起始位置
    "pageSize": 0,  # 每页查询记录数
    "status": 0,  # 状态
    "userId": "",  # 用户Id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_download_recordeList(data=data, headers=headers):
    """
    分页获取下载列表
    /mgmt/download/recordeList

    参数说明:
    - pageNum: 分页查询起始位置
    - pageSize: 每页查询记录数
    - status: 状态
    - userId: 用户Id
    """

    url = "/mgmt/download/recordeList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
