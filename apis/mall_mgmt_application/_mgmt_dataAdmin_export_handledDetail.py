import os

from util.client import client

data = {
    "day": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_handledDetail(data=data, headers=headers):
    """
    经办人明细导出
    /mgmt/dataAdmin/export/handledDetail
    """

    url = "/mgmt/dataAdmin/export/handledDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
