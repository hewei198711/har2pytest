import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadStoreSingleSignContractTemplate(headers=headers):
    """
    下载服务中心单方签署合同导入模板(无文件版)
    /mgmt/store/downloadStoreSingleSignContractTemplate
    """

    url = "/mgmt/store/downloadStoreSingleSignContractTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
