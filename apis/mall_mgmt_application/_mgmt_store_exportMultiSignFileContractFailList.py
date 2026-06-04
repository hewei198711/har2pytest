import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportMultiSignFileContractFailList(headers=headers):
    """
    导出多方签署合同导入失败列表(文件版)
    /mgmt/store/exportMultiSignFileContractFailList
    """

    url = "/mgmt/store/exportMultiSignFileContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
