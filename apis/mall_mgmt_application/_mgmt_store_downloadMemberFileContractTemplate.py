import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadMemberFileContractTemplate(headers=headers):
    """
    下载会员双方签署合同导入模板(文件版)
    /mgmt/store/downloadMemberFileContractTemplate
    """

    url = "/mgmt/store/downloadMemberFileContractTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
