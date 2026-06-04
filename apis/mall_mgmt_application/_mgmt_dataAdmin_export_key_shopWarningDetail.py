import os

from util.client import client

data = {
    "customerCard": "",  # TODO: 添加参数说明
    "customerName": "",  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # TODO: 添加参数说明
    "placeMonthStr": "",  # TODO: 添加参数说明
    "registerPhone": "",  # TODO: 添加参数说明
    "ruleId": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_key_shopWarningDetail(data=data, headers=headers):
    """
    重点购货预警列表导出
    /mgmt/dataAdmin/export/key/shopWarningDetail
    """

    url = "/mgmt/dataAdmin/export/key/shopWarningDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
