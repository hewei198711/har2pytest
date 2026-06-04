import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportContractFileFailList(headers=headers):
    """
    导出双方签署合同导入失败列表(文件版)
    /mgmt/store/exportContractFileFailList
    """

    url = "/mgmt/store/exportContractFileFailList"
    with client.get(url=url, headers=headers) as r:
        return r
