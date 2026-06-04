import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreSingleFileContractFailList(headers=headers):
    """
    导出服务中心单方签署合同导入失败列表(文件版)
    /mgmt/store/exportStoreSingleFileContractFailList
    """

    url = "/mgmt/store/exportStoreSingleFileContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
