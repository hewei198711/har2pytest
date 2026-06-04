import os

from util.client import client

data = {
    "centerCode": "",  # TODO: 添加参数说明
    "centerName": "",  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # TODO: 添加参数说明
    "placeMonthStr": "",  # TODO: 添加参数说明
    "ruleId": 0,  # TODO: 添加参数说明
    "statisticId": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_deliverWarningDetail(data=data, headers=headers):
    """
    交付预警列表导出
    /mgmt/dataAdmin/export/deliverWarningDetail
    """

    url = "/mgmt/dataAdmin/export/deliverWarningDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
