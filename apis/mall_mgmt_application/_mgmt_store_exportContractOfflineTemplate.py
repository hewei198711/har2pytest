import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportContractOfflineTemplate(headers=headers):
    """
    下载线下合同导入模板
    /mgmt/store/exportContractOfflineTemplate
    """

    url = "/mgmt/store/exportContractOfflineTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
