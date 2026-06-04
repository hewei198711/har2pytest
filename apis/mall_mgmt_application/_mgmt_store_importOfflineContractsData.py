import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importOfflineContractsData(headers=headers):
    """
    导入线下合同数据
    /mgmt/store/importOfflineContractsData
    """

    url = "/mgmt/store/importOfflineContractsData"
    with client.post(url=url, headers=headers) as r:
        return r
