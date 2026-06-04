import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeContractBankCard_exportFailList(headers=headers):
    """
    对公签约银行卡管理失败记录
    /mgmt/store/storeContractBankCard/exportFailList
    """

    url = "/mgmt/store/storeContractBankCard/exportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
