import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportMemberSingleFileContractFailList(headers=headers):
    """
    导出会员单方签署合同导入失败列表(文件版)
    /mgmt/store/exportMemberSingleFileContractFailList
    """

    url = "/mgmt/store/exportMemberSingleFileContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
