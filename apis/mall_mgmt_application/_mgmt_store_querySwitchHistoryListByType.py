import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "switchType": 0,  # 开关类型：1、钱包对账单开关
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_querySwitchHistoryListByType(params=params, headers=headers):
    """
    通过类型查询开关历史记录
    /mgmt/store/querySwitchHistoryListByType

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - switchType: 开关类型：1、钱包对账单开关
    """

    url = "/mgmt/store/querySwitchHistoryListByType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
