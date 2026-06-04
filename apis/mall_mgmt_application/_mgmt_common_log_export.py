import os

from util.client import client

data = {
    "content": "",  # TODO: 添加参数说明
    "endTime": 0,  # TODO: 添加参数说明
    "module": "",  # TODO: 添加参数说明
    "operator": "",  # TODO: 添加参数说明
    "startTime": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_common_log_export(data=data, headers=headers):
    """
    操作日志-批量导出
    /mgmt/common/log/export
    """

    url = "/mgmt/common/log/export"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
