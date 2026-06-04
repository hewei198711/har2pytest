import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreEditLog(params=params, headers=headers):
    """
    服务中心详情 -- 变更历史导出
    /mgmt/store/exportStoreEditLog

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/exportStoreEditLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
