import os

from util.client import client

params = {
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


def _mgmt_msgadmin_handmade_downloadReceiverList(params=params, headers=headers):
    """
    导出发送名单
    /mgmt/msgadmin/handmade/downloadReceiverList
    """

    url = "/mgmt/msgadmin/handmade/downloadReceiverList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
