import os

from util.client import client

data = {
    "cardNo": "",  # TODO: 添加参数说明
    "fileName": "",  # TODO: 添加参数说明
    "keyWord": "",  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "planCode": "",  # TODO: 添加参数说明
    "serverNo": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_receiverList(data=data, headers=headers):
    """
    导入名单列表
    /mgmt/msgadmin/handmade/receiverList
    """

    url = "/mgmt/msgadmin/handmade/receiverList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
