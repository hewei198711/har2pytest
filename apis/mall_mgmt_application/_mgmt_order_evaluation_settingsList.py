import os

from util.client import client

data = {
    "pageNum": 0,  # 页码 默认1
    "pageSize": 0,  # 页数 默认10
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_evaluation_settingsList(data=data, headers=headers):
    """
    获取评价时限设置列表
    /mgmt/order/evaluation/settingsList

    参数说明:
    - pageNum: 页码 默认1
    - pageSize: 页数 默认10
    """

    url = "/mgmt/order/evaluation/settingsList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
