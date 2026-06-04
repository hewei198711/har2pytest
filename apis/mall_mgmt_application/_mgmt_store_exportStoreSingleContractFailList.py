import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreSingleContractFailList(headers=headers):
    """
    导出服务中心单方签署合同导入失败列表(无文件版)
    /mgmt/store/exportStoreSingleContractFailList
    """

    url = "/mgmt/store/exportStoreSingleContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
