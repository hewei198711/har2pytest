import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadMultiSignFileContractTemplate(headers=headers):
    """
    下载多方签署合同导入模板(文件版)
    /mgmt/store/downloadMultiSignFileContractTemplate
    """

    url = "/mgmt/store/downloadMultiSignFileContractTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
