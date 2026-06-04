import os

from util.client import client

params = {
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


def _mgmt_dataAdmin_keyShopWarningDetail_list(params=params, headers=headers):
    """
    数据中心管理后台-重点名单购货预警管理-获取重点购货预警列表
    /mgmt/dataAdmin/keyShopWarningDetail/list
    """

    url = "/mgmt/dataAdmin/keyShopWarningDetail/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
