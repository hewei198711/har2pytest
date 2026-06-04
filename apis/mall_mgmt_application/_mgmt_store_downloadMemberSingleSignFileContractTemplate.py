import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadMemberSingleSignFileContractTemplate(headers=headers):
    """
    下载会员单方签署合同导入模板(文件版)
    /mgmt/store/downloadMemberSingleSignFileContractTemplate
    """

    url = "/mgmt/store/downloadMemberSingleSignFileContractTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
