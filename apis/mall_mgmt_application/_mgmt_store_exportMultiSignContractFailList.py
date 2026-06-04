import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportMultiSignContractFailList(headers=headers):
    """
    导出多方签署合同导入失败列表
    /mgmt/store/exportMultiSignContractFailList
    """

    url = "/mgmt/store/exportMultiSignContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
