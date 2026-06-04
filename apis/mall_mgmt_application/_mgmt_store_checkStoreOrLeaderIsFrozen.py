import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkStoreOrLeaderIsFrozen(headers=headers):
    """
    根据storeCode列表查询服务中心或负责人状态是否冻结，冻结则返回true，否则返回false
    /mgmt/store/checkStoreOrLeaderIsFrozen
    """

    url = "/mgmt/store/checkStoreOrLeaderIsFrozen"
    with client.get(url=url, headers=headers) as r:
        return r
