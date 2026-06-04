import os

from util.client import client

data = {
    "boardName": "",  # TODO: 添加参数说明
    "createTime": "",  # TODO: 添加参数说明
    "createTimeStr": "",  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "status": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_realtimeBoardList(data=data, headers=headers):
    """
    实时数据看板列表
    /mgmt/dataAdmin/export/realtimeBoardList
    """

    url = "/mgmt/dataAdmin/export/realtimeBoardList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
