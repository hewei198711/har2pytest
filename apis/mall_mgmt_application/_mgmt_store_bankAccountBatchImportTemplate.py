import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_bankAccountBatchImportTemplate(headers=headers):
    """
    批量添加银行账号模板下载
    /mgmt/store/bankAccountBatchImportTemplate
    """

    url = "/mgmt/store/bankAccountBatchImportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
