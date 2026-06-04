import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_storeContractBankCard_batchImport(headers=headers):
    """
    对公签约银行卡管理批量导入
    /mgmt/store/storeContractBankCard/batchImport
    """

    url = "/mgmt/store/storeContractBankCard/batchImport"
    with client.post(url=url, headers=headers) as r:
        return r
