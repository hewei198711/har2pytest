import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeEditLog(params=params, headers=headers):
    """
    服务中心详情 -- 变更历史
    /mgmt/store/storeEditLog

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: storeCode
    """

    url = "/mgmt/store/storeEditLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
