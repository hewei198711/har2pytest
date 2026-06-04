import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportOfflineContractFailList(headers=headers):
    """
    导出线下合同失败列表
    /mgmt/store/exportOfflineContractFailList
    """

    url = "/mgmt/store/exportOfflineContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
